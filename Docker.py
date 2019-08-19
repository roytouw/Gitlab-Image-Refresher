import docker
from Exceptions import ImageNotFoundException, FailedUpdatingContainerException, FailedCleaningServiceException, \
    FailedUpdatingServiceException
from Logger import Logger

client = docker.from_env()
logger = Logger()


# Pull image from given location.
def refresh_image(location):
    try:
        logger.log_line(f'Pulling image {location}, this may take a while.')
        client.images.pull(location)
        logger.log_line(f'Pulled image {location}')
    except Exception:
        raise ImageNotFoundException(f'Image not found at {location}!')


# Restart all containers running an old version of the passed image.
def restart_outdated_containers(location, revision):
    try:
        restarted = False
        containers = client.containers.list(all=True)
        for container in containers:
            service = container.attrs.get('Config').get('Labels').get('com.docker.stack.namespace')
            if service is not None:  # Container belongs to service.
                continue
            image_path = container.attrs.get('Config').get('Image')
            image_revision = container.attrs.get('Image').split(":")[1]
            if location == image_path:
                if revision != image_revision:      # Running old version of image.
                    if container.attrs.get('State').get('Running'):
                        container.stop()
                    container.remove()
                    client.containers.run(location, detach=True)
                    restarted = True
                    logger.log_line(f'Restarted container {location}')
        return restarted
    except Exception as error:
        logger.log_line(f'Failed restarting container {location}!')
        raise FailedUpdatingContainerException(error)


# Run image in a container once.
def run_image_once(location):
    return False


# Remove stopped containers belonging to service.
def cleanup_service(service_name):
    try:
        containers = client.containers.list(all=True)
        for container in containers:
            containing_service = container.attrs.get('Config').get('Labels').get('com.docker.swarm.service.name')
            if containing_service == service_name:
                if not container.attrs.get('State').get('Running'):     # If not running.
                    container.remove()
    except Exception as error:
        logger.log_line(f'Failed cleaning up service {service_name}!')
        raise FailedCleaningServiceException(error)


# Force update all services with an image of given location.
def restart_services(location):
    try:
        services = client.services.list()
        for service in services:
            service_image_location = service.attrs.get('Spec').get('Labels').get('com.docker.stack.image')
            if service_image_location == location:
                service_name = service.attrs.get('Spec').get('Name')
                service.force_update()
                cleanup_service(service_name)
                logger.log_line(f'Service {location} updated.')
    except Exception as error:
        logger.log_line(f'Failed restarting service {location}!')
        raise FailedUpdatingServiceException(error)


# if __name__ == '__main__':
    # containers = client.containers.list(all=True)
    # for container in containers:
    #     print(container.attrs.get('Config').get('Labels').get('com.docker.stack.namespace') == None)
    # # print(restart_services('test'))
