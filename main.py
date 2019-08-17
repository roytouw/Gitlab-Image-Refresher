import time

from ConfigReader import ConfigReader
from GitlabAPI import get_image_info
from caching import Cacher
from Exceptions import ErrorConnectingAPIException, ImageNotFoundException
from Docker import refresh_image, restart_outdated_containers

config_reader = ConfigReader()
cacher = Cacher()
registries = config_reader.get_registries()


def register_images():
    for registry in registries:
        for image in registry['images']:
            image_info = get_image_info(registry['user'], registry['project'], image['tag'])
            if image_info.get('error'):
                raise ErrorConnectingAPIException('Could not connect to API!')
            cacher.update_or_insert_image(image_info['path'], image_info['revision'])


def poll_updates():
    try:
        while True:
            for registry in registries:
                for image in registry['images']:
                    image_info = get_image_info(registry['user'], registry['project'], image['tag'])
                    image_cache = cacher.search_image(image_info['path'])[0]

                    if image_cache['revision'] != image_info['revision']:
                        cacher.update_image(image_info['path'], image_info['revision'])
                        refresh_image(image_info['location'])
                        restart_outdated_containers(image_info['location'], image_info['revision'])
                    else:
                        print('No update.')
            time.sleep(config_reader.get_interval())
    except ImageNotFoundException as error:
        print(error)  # TODO Should log this


if __name__ == '__main__':
    # register_images()
    poll_updates()
