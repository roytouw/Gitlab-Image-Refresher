import docker
from Exceptions import ImageNotFoundException

client = docker.from_env()


# Pull image from given location.
def refresh_image(location):
    try:
        client.images.pull(location)
    except Exception:
        raise ImageNotFoundException(f'Image not found at {location}!')


# Restart all containers running an old version of the passed image.
def restart_outdated_containers(location, revision):
    restarted = False
    containers = client.containers.list(all=True)
    for container in containers:
        image_path = container.attrs.get('Config').get('Image')
        image_revision = container.attrs.get('Image').split(":")[1]
        if location == image_path:
            if revision != image_revision or True:      # Running old version of image.
                container.stop()
                container.remove()
                client.containers.run(location, detach=True)
                restarted = True
                print(f'Restarted container {location}')
    return restarted


if __name__ == '__main__':
    restart_outdated_containers('test', 'revision')