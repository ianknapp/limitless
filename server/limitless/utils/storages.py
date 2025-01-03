from django.conf import settings
from s3file.storages_optimized import S3OptimizedUploadStorage
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIAFILES_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class PrivateLargeMediaStorage(S3OptimizedUploadStorage):
    default_acl = "private"
    file_overwrite = False
    custom_domain = False
