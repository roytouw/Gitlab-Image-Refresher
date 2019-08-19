import time

from ConfigReader import ConfigReader
from GitlabAPI import get_image_info
from caching import Cacher
from Exceptions import ErrorConnectingAPIException, ImageNotFoundException
from Docker import refresh_image, restart_outdated_containers, restart_services, run_image_once, cleanup_exited_containers
from Logger import Logger

config_reader = ConfigReader()
cacher = Cacher()
registries = config_reader.get_registries()
logger = Logger()


def register_images():
    for registry in registries:
        for image in registry['images']:
            image_info = get_image_info(registry['user'], registry['project'], image['tag'], registry['apiToken'])
            if image_info.get('error'):
                raise ErrorConnectingAPIException('Could not connect to API!')
            cacher.update_or_insert_image(image_info['path'], image_info['revision'])
            refresh_image(image_info['location'])
            restart_services(image_info['location'])
            restart_outdated_containers(image_info['location'], image_info['revision'])
            cleanup_exited_containers()
            logger.log_line(f'Registered and updated image {image_info["location"]}')


def poll_updates():
    try:
        while True:
            for registry in registries:
                for image in registry['images']:
                    try:
                        image_info = get_image_info(registry['user'], registry['project'], image['tag'], registry['apiToken'])
                        image_cache = cacher.search_image(image_info['path'])[0]

                        if image_cache['revision'] != image_info['revision']:
                            logger.log_line(f'Update detected for image {image_info["location"]}')
                            cacher.update_image(image_info['path'], image_info['revision'])
                            refresh_image(image_info['location'])
                            restarted_as_service = restart_services(image_info['location'])
                            restarted_as_container = restart_outdated_containers(image_info['location'], image_info['revision'])
                            cleanup_exited_containers()

                            if not restarted_as_service or restarted_as_container:
                                run_image_once(image_info['location'])
                            print(f'Updated {image_info["location"]}')
                        else:
                            print('No update.')
                    except Exception as error:
                        logger.log_line(error)
                        continue
            time.sleep(config_reader.get_interval())
    except ImageNotFoundException as error:
        logger.log_line(error)


if __name__ == '__main__':
    register_images()
    poll_updates()
