import time

from ConfigReader import ConfigReader
from GitlabAPI import get_image_info
from caching import Cacher

config_reader = ConfigReader()
cacher = Cacher()
registries = config_reader.get_registries()


def register_images():
    for registry in registries:
        for image in registry['images']:
            image_info = get_image_info(registry['user'], registry['project'], image['tag'])
            cacher.update_or_insert_image(image_info['path'], image_info['revision'])


def poll_updates():
    while True:
        for registry in registries:
            for image in registry['images']:
                image_info = get_image_info(registry['user'], registry['project'], image['tag'])
                image_cache = cacher.search_image(image_info['path'])[0]

                if image_cache['revision'] != image_info['revision']:
                    cacher.update_image(image_info['path'], image_info['revision'])
                    print('Update detected!')
                else:
                    print('No update.')
        time.sleep(config_reader.get_interval())


register_images()
poll_updates()
