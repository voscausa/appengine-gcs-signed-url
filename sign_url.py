#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2
import time
import urllib
from datetime import datetime, timedelta
from google.appengine.api import app_identity
import os
import base64
import logging

GCS_API_ACCESS_ENDPOINT = 'https://storage.googleapis.com'

# Use the default bucket in the cloud and not the local SDK one from app_identity
default_bucket = '%s.appspot.com' % os.environ['APPLICATION_ID'].split('~', 1)[1]
google_access_id = app_identity.get_service_account_name()


def sign_url(bucket_object, expires_after_seconds=6, bucket=default_bucket):
    """ cloudstorage signed url to download cloudstorage object without login
        Docs : https://cloud.google.com/storage/docs/access-control?hl=bg#Signed-URLs
        API : https://cloud.google.com/storage/docs/reference-methods?hl=bg#getobject
    """

    method = 'GET'
    gcs_filename = urllib.quote('/%s/%s' % (bucket, bucket_object))
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
        gcs_filename])

    signature_bytes = app_identity.sign_blob(signature_string)[1]

    # Set the right query parameters. we use a gae service account for the id
    query_params = {'GoogleAccessId': google_access_id,
                    'Expires': str(expiration),
                    'Signature': base64.b64encode(signature_bytes)}

    # Return the built URL.
    result = '{endpoint}{resource}?{querystring}'.format(endpoint=GCS_API_ACCESS_ENDPOINT,
                                                         resource=gcs_filename,
                                                         querystring=urllib.urlencode(query_params))
    return result


class SignUrl(webapp2.RequestHandler):

    def get(self,  bucket_object=None):
        """ create a signed url when the download link is clicked and redirect instantly """

        if bucket_object:
            signed_url = sign_url(bucket_object, expires_after_seconds=7200)
            response = self.redirect(signed_url)
            logging.info(response)
        else:
            self.abort(400)


class DownloadSigned(webapp2.RequestHandler):
    """ create a download link, which will not expire"""

    def get(self):
        """ create a signed url when the link is clicked to download the bucket_object """

        bucket_object = self.request.get('bucket_object', default_value=None)
        if not bucket_object:
            self.response.write('<p>No value provided for argument bucket_object</p>')
        else:
            self.response.write('<p>Download : <a href="/sign_url/%s">%s</a> using a signed url</p>'
                                % (bucket_object, bucket_object))
