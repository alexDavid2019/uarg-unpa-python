
#Constantes utilizadas para consumir los servicios en la api

HOST_API = "http://localhost:8085"

OCSP_REQ_TYPE = 'application/ocsp-request'
OCSP_REP_TYPE = 'application/ocsp-response'
JSON_REQ_TYPE = 'application/json'

ENDPOINT_GET_HEALTH = '/health'

ENDPOINT_GET_TIMESTAMP = '/timestamp'
ENDPOINT_GET_CRT = '/crt'
ENDPOINT_GET_CRL = '/crl'

ENDPOINT_GET_CERTIFICATE_BY_CUIT_CERTID = '/api/v1/certificate/[cuit]/[id]'
ENDPOINT_GET_CERTIFICATE_BY_CUIT = '/api/v1/allCertificate/[cuit]'
ENDPOINT_GET_DOCUMENTS_BY_CUIT = '/api/v1/allDocuments/[cuit]'
ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID = '/api/v1/document/[cuit]/[id]'

ENDPOINT_POST_SIGN_DOCUMENT = '/api/v1/signDocument'
ENDPOINT_POST_UPLOAD_DOCUMENT = '/api/v1/uploadDocument'
ENDPOINT_POST_SIGN = '/api/v1/sign'
ENDPOINT_POST_LOGIN = '/api/v1/login'
ENDPOINT_POST_OCSP = '/'
