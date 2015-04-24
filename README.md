# appengine-gcs-signed-url
Signed url creation to download a Google Cloudstorage object on appengine

The App Engine SDK supports the Cloud Storage Client. It doesn't support the cloudstoge REST API's.  
But the SDK can use a service account to access the hosted Cloud storage.
An appengine service accounts makes it very easy to use OAuth2 and Python APIs.  
To make this work in the SDK, you have to use two options in development server:

    --appidentity_email_address=<developer service account e-mail address>
    --appidentity_private_key_path=<d:/.../gcs-blobstore.pem key>
    
The service account e-mail and a p12 key can be found in the Google Developers Console of your Cloud project:

    Google Developers Console -> API & Auth -> Create a new client ID for a service account and generate p12 key

Use openssl to convert the p12 in a RSA pem key. For windows use:

    openssl pkcs12 -in gcs-blobstore.p12  -nocerts -nodes -passin pass:notasecret | openssl rsa -out gcs-blobstore.pem

[More docs about the service account SDK options](https://gist.github.com/pwalsh/b8563e1a1de3347a8066)
