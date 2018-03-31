import json
import urlparse
from StringIO import StringIO
from swiftclient.service import SwiftService, SwiftUploadObject, SwiftError


from anchore_engine.subsys.object_store.drivers.interface import ObjectStorageDriver
from anchore_engine.subsys.object_store.exc import DriverBackendError, DriverConfigurationError, ObjectKeyNotFoundError, ObjectStorageDriverError
from anchore_engine.subsys import logger


# Deal with the verbose logging verbosity of swiftclient
import logging
l = logging.getLogger('swiftclient')
l.setLevel(logging.WARN)


class SwiftObjectStorageDriver(ObjectStorageDriver):
    """
    Archive driver using swift-api as backing store.

    Buckets presented as part of object lookup in this API are mapped to object key prefixes in the backing S3 store so that a single bucket (or set of buckets)
    can be used since namespaces are limited.

    """
    __config_name__ = 'swift'
    __driver_version__ = '1'
    __uri_scheme__ = 'swift'

    _key_format = '{prefix}{userid}/{bucket}/{key}'
    DEFAULT_AUTH_TIMEOUT = 10

    def __init__(self, config):
        super(SwiftObjectStorageDriver, self).__init__(config)

        # Initialize the client
        self.client_config = config
        self.bucket_name = self.config.get('bucket')
        self.client = SwiftService(options=self.client_config)

        if not self.bucket_name:
            raise ValueError('Cannot configure s3 driver with out a provided bucket to use')

        self.prefix = self.config.get('anchore_key_prefix', '')

    def _build_key(self, userId, usrBucket, key):
        return self._key_format.format(prefix=self.prefix, userid=userId, bucket=usrBucket, key=key)

    def _parse_uri(self, uri):
        parsed = urlparse.urlparse(uri, scheme=self.__uri_scheme__)
        bucket = parsed.hostname
        key = parsed.path[1:] # Strip leading '/'
        return bucket, key

    def get_by_uri(self, uri):
        try:
            bucket, key = self._parse_uri(uri)
            if bucket != self.bucket_name:
                logger.warn('Bucket mismatch between content_uri and configured bucket name: {} in db record, but {} in config'.format(bucket, self.bucket_name))

            resp = self.client.download(container=bucket, objects=[key], options={'out_file': '-'})
            for obj in resp:
                if 'contents' in obj and obj['action'] == 'download_object':
                    content = ''.join(obj['contents'])
                    return content
                elif obj['action'] == 'download_object' and not obj['success']:
                    raise ObjectKeyNotFoundError(bucket='', key='', userId='', caused_by=None)
                raise Exception('Unexpected operation/action from swift: {}'.format(obj['action']))
        except SwiftError as e:
            raise ObjectStorageDriverError(cause=e)

    def delete_by_uri(self, uri):
        try:
            bucket, key = self._parse_uri(uri)
            if bucket != self.bucket_name:
                logger.warn('Bucket mismatch between content_uri and configured bucket name: {} in db record, but {} in config'.format(bucket, self.bucket_name))

            resp = self.client.delete(container=self.bucket_name, objects=[key])
            for r in resp:
                if r['success'] and r['action'] == 'delete_object':
                    return True
        except Exception as e:
            raise e

    def exists(self, uri):
        try:
            bucket, key = self._parse_uri(uri)
            if bucket != self.bucket_name:
                logger.warn('Bucket mismatch between content_uri and configured bucket name: {} in db record, but {} in config'.format(bucket, self.bucket_name))

            resp = self.client.download(container=bucket, objects=[key], options={'out_file': '-', 'no_download': True})
            for obj in resp:
                if 'success' in obj and obj['success'] and obj['action'] == 'download_object':
                    return True
                elif obj['action'] == 'download_object' and not obj['success']:
                    return False
                raise Exception('Unexpected operation/action from swift: {}'.format(obj['action']))
        except SwiftError as e:
            raise ObjectStorageDriverError(cause=e)

    def get(self, userId, bucket, key):
        return self.get_by_uri(self.uri_for(userId, bucket, key))

    def put(self, userId, bucket, key, data):
        try:
            uri = self.uri_for(userId, bucket, key)
            swift_bucket, swift_key = self._parse_uri(uri)
            obj = SwiftUploadObject(object_name=swift_key, source=StringIO(data))
            resp = self.client.upload(container=swift_bucket, objects=[obj])
            for upload in resp:
                if upload['action'] == 'upload_object' and upload['success']:
                    return uri
            else:
                raise Exception('Failed uploading object to swift')
        except Exception as e:
            raise e

    def delete(self, userId, bucket, key):
        return self.delete_by_uri(self.uri_for(userId, bucket, key))

    def uri_for(self, userId, bucket, key):
        return '{}://{}/{}'.format(self.__uri_scheme__, self.bucket_name, self._build_key(userId, bucket, key))