#!/usr/bin/python
# -*- coding: utf-8 -*-

import webapp2

routes = [
    webapp2.Route(r'/download_signed', handler='sign_url.DownloadSigned'),
    webapp2.Route(r'/sign_url/<bucket_object:.*>', handler='sign_url.SignUrl'),
]
app = webapp2.WSGIApplication(routes=routes, debug=True)
