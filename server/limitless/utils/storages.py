import os

from storages.utils import clean_name, ReadBytesWrapper, is_seekable
from django.conf import settings
from s3file.storages_optimized import S3OptimizedUploadStorage
from storages.backends.s3boto3 import S3Boto3Storage


class PrivateMediaStorage(S3Boto3Storage):
    location = settings.PRIVATE_MEDIAFILES_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False


class PrivateLargeMediaStorage(S3OptimizedUploadStorage):
    location = settings.PRIVATE_MEDIAFILES_LOCATION
    default_acl = "private"
    file_overwrite = False
    custom_domain = False

    def _save(self, name, content):
        # Basically copy the implementation of _save of S3Boto3Storage
        # and replace the obj.upload_fileobj with a copy function
        cleaned_name = clean_name(name)
        name = self._normalize_name(cleaned_name)
        params = self._get_write_parameters(name, content)

        if is_seekable(content):
            content.seek(0, os.SEEK_SET)

        # wrap content so read() always returns bytes. This is required for passing it
        # to obj.upload_fileobj() or self._compress_content()
        content = ReadBytesWrapper(content)

        if (
            self.gzip
            and params["ContentType"] in self.gzip_content_types
            and "ContentEncoding" not in params
        ):
            content = self._compress_content(content)
            params["ContentEncoding"] = "gzip"

        obj = self.bucket.Object(name)
        # content.seek(0, os.SEEK_SET)  # Disable unnecessary seek operation
        # obj.upload_fileobj(content, ExtraArgs=params)  # Disable upload function

        if not hasattr(content, "obj") or not hasattr(content.obj, "key"):
            raise TypeError(
                "The content object must be a S3 object and contain a valid key."
            )

        # Copy the file instead uf uploading
        obj.copy({"Bucket": self.bucket.name, "Key": content.obj.key}, ExtraArgs=params)

        return cleaned_name
