#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
import time
import urllib
from datetime import datetime, timedelta
from google.appengine.api import app_identity
import os
import base64

API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'

# Use the default bucket in the cloud and not the local SDK one from app_identity
default_bucket = '%s.appspot.com' % os.environ['APPLICATION_ID'].split('~', 1)[1]
google_access_id = app_identity.get_service_account_name()


def sign_url(bucket_object, expires_after_seconds=60, bucket=default_bucket):
    """ cloudstorage signed url to download cloudstorage object without login
        Docs : https://cloud.google.com/storage/docs/access-control?hl=bg#Signed-URLs
        API : https://cloud.google.com/storage/docs/reference-methods?hl=bg#getobject
    """

    method = 'GET'
    gcs_filename = '/%s/%s' % (bucket, bucket_object)
    content_md5, content_type = None, None

    # expiration : number of seconds since epoch
    expiration_dt = datetime.utcnow() + timedelta(seconds=expires_after_seconds)
    expiration = int(time.mktime(expiration_dt.timetuple()))

    # Generate the string to sign.
    signature_string = '\n'.join([
        method,
        content_md5 or '',
        content_type or '',
        str(expiration),
        str(gcs_filename)])

    _, signature_bytes = app_identity.sign_blob(signature_string)

    # Set the right query parameters. we use a gae service account for the id
    query_params = {'GoogleAccessId': google_access_id,
                    'Expires': str(expiration),
                    'Signature': base64.b64encode(signature_bytes)}

    # Return the built URL.
    return '{endpoint}{resource}?{querystring}'.format(endpoint=API_ACCESS_ENDPOINT,
                                                       resource=str(gcs_filename),
                                                       querystring=urllib.urlencode(query_params))


class SignUrl(webapp2.RequestHandler):
    """ create signed url for a cloudstorage object to download """

    def get(self):

        bucket_object = self.request.get('bucket_object', default_value=None)
        if not bucket_object:
            self.response.write('<p>No value provided for argument bucket_object</p>')
            return

        signed_url = sign_url(bucket_object, expires_after_seconds=7200)

        self.response.write('<p>SignUrl finished. Download : <a href="%s">%s</a></p>' % (signed_url, bucket_object))
