class UserNotFoundException(Exception):
    pass


class ProjectNotFoundException(Exception):
    pass


class RepositoryNotFoundException(Exception):
    pass


class ErrorConnectingAPIException(Exception):
    pass


class ImageNotFoundException(Exception):
    pass


class FailedUpdatingContainerException(Exception):
    pass


class FailedUpdatingServiceException(Exception):
    pass


class FailedCleaningServiceException(Exception):
    pass


class FailedRemovingContainerException(Exception):
    pass
