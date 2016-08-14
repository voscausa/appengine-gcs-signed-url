# appengine-gcs-signed-url
Signed url creation to download a Google Cloudstorage object on appengine

The App Engine SDK supports the Cloud Storage Client. It doesn't support the cloudstorage REST API's.  
But the SDK can use a service account to access the hosted Cloud storage.
An appengine service accounts makes it very easy to use OAuth2 and Python APIs.  
To make this work in the SDK, you have to use two options in development server:

    --appidentity_email_address=<developer service account e-mail address>
    --appidentity_private_key_path=<d:/.../<pem key filename>
    
The service account e-mail and a p12 key can be found in the [Google Developers Console](https://console.cloud.google.com/permissions/serviceaccounts?project=) of your Cloud project:

    Cloud Console -> Permissions -> Service Accounts to create a service account and p12 key  

Use openssl to convert the p12 in a RSA pem key. For windows use:

    openssl pkcs12 -in <p12 key filename>  -nocerts -nodes -passin pass:notasecret | openssl rsa -out <pem key filename>
    
I used [this link](http://slproweb.com/products/Win32OpenSSL.html) to install OpenSSL

[More docs about the service account SDK options](https://gist.github.com/pwalsh/b8563e1a1de3347a8066)
