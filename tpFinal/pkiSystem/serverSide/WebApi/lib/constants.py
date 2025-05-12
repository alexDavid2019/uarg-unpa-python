
#Constantes utilizadas al momento de la generacion de certificados (init() method)

#definimos constantes con sus correspondientes tipos.
COUNTRY = str = "AR"
STATE = str = "Buenos Aires"
CITY = str = "CABA"
KEY_LEN_RSA = int = 4096
HASH_ALGORITHM = str = "sha512" 
CA_ORGANIZATION_NAME = str = "Infraestructura de Firma Digital de la República Argentina"
CA_DEPARMENT_NAME = str = "Infraestructura de Firma Digital"
OCSP_ORGANIZATION_NAME = str = "OCSP Infraestructura de Firma Digital"
OCSP_DEPARMENT_NAME = str = "OCSP Signing Certificate Request"
OCSP_KEY_LEN_RSA = int = 2048
OCSP_HASH_ALGORITHM = str = "sha256" 

#Los puertos deben pertenecer a nuestra WebApi
URI_OCSP = str = "http://localhost:8085"
URI_CA_CRT = str = "http://localhost:8085/crt"
URI_CRL = str = "http://localhost:8085/crl"

#Constantes utilizadas para exponer servicios en la api (main() method)

PORT = 8085

OCSP_REQ_TYPE = 'application/ocsp-request'
OCSP_REP_TYPE = 'application/ocsp-response'
JSON_REQ_TYPE = 'application/json'


ENDPOINT_GET_HEALTH = '/health'

ENDPOINT_GET_TIMESTAMP = '/timestamp'
ENDPOINT_GET_CRT = '/crt'
ENDPOINT_GET_CRL = '/crl'

ENDPOINT_GET_CERTIFICATE_BY_CUIT = '/api/v1/allCertificate/([0-9-]+)'
ENDPOINT_GET_DOCUMENTS_BY_CUIT = '/api/v1/allDocuments/([0-9-]+)'
ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID = '/api/v1/document/([0-9-]+)/([0-9-]+)'
ENDPOINT_GET_CERTIFICATE_BY_CUIT_CERTID = '/api/v1/certificate/([0-9-]+)/([0-9-]+)'

ENDPOINT_POST_SIGN_DOCUMENT = '/api/v1/signDocument'
ENDPOINT_POST_UPLOAD_DOCUMENT = '/api/v1/uploadDocument'
ENDPOINT_POST_SIGN = '/api/v1/sign'
ENDPOINT_POST_LOGIN = '/api/v1/login'
ENDPOINT_POST_OCSP = '/'

