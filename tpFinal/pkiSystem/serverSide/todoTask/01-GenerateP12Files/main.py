'''
CONSIGNA:
    Toda PKI necesita ofrecer como producto base, los certificados digitales propios.
    Para eso, se requiere generar los certificados digitales utilizando en este momento la herramienta openssl.
    Se necesita saber lo siguiente:
    - Archivos PEM correspondiente a una CA raiz sobre el cual se generan los pkcs12 hijos (ruta de confianza).
    - Composicion del certificado raiz CA.
        - Algoritmo de firma: SHA512 RSA
        - Emisor / Sujeto:
            CN = AC Raíz de la República Argentina
            O = Infraestructura de Firma Digital de la República Argentina
            C = AR
        - Longitud clave publica: 2048 bits
        - Restricciones para su uso:
                Firma de certificados, Firma CRL sin conexión, Firma de lista de revocación de certificados (CRL) (06)
        - Periodo de vigencia: 3650 dias.
    - Generar el PKCS7 ()    

'''
'''
# MODELO

Clases:

Acciones:

'''
"""
Recomendaciones para el orden de importacion:
"""
#1. Librerias standard
import sys
import os
import time 
import logging
import random
from socket import gethostname
from datetime import datetime

#2. Librerias de terceros
#!pip install pyOpenSSL
from OpenSSL import crypto
# python3 -m pip install rsa #https://github.com/sybrenstuvel/python-rsa
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.x509 import ocsp
from cryptography.x509.ocsp import OCSPResponseStatus
from cryptography.x509.oid import ExtensionOID, AuthorityInformationAccessOID


#3. Librerias propias
from custom_logger import getLogger
#from generate_csr_rsa_files import getGenerateCSRSigned
from generate_ca_csr_files import getGenerateCA,getGenerateCSRSigned
from generate_cert_files import getGenerateCertificate,getGenerateOcspResponseCertificate
from custom_certUtil import export_to_pkcs12,load_private_key,load_certificate
from custom_fileIO import writeFile,cleanFolderForFile

logger = logging.getLogger('root')

hash_algorithm = "sha512RSA" 

certsRepo = "filesRepo"

county = "AR"
state = "Buenos Aires"
city = "CABA"

issuer_name_organization = "Infraestructura de Firma Digital de la República Argentina"
issuer_name_department = "Infraestructura de Firma Digital"


def main():

    fileNameToWrite = "%s-%d" %("caAutoSigned", time.time())
    #return tuple
    caCertFile,caKeyCertFile = getGenerateCA(certsRepo,fileNameToWrite,"My First CA Certificate")
    #caCertFile = os.path.join(certsRepo, fileNameToWrite + '.crt')    
    #caKeyCertFile = os.path.join(certsRepo, fileNameToWrite + '.key')    

    #Por cada certificado 'cliente' de nuestra 'CA', se genera el CSR y su correspondiente CER

    fileNameToWrite = "%s-%d" %("csrFile", time.time())
    #return tuple
    csrFileGenerated,csrKeyFileGenerated=getGenerateCSRSigned(certsRepo, fileNameToWrite,caCertFile,'localhost',issuer_name_organization,issuer_name_department)
    #csrFileGenerated = os.path.join(certsRepo, fileNameToWrite + '.csr')
    #csrKeyFileGenerated = os.path.join(certsRepo, fileNameToWrite + '.key')    

    fileNameToWrite = "%s-%d" %("certificateFile", time.time())
    #return tuple
    cerFileGenerated, cerMergedCA = getGenerateCertificate(certsRepo,fileNameToWrite,"localhost",caCertFile,caKeyCertFile,csrFileGenerated,csrKeyFileGenerated)
    #cerFileGenerated = os.path.join(certsRepo, fileNameToWrite + '.cer')

    fileNameToWrite = "%s-%d" %("ocsp_certificateResponse", time.time())
    #return tuple
    ocspFileGenerated, ocspKeyFileGenerated = getGenerateOcspResponseCertificate(certsRepo,fileNameToWrite,"localhost",caCertFile,caKeyCertFile)

    # show our certificate file
    certfile = open(cerFileGenerated, 'r')
    cert_data = certfile.read()
    certfile.close()
    print(cert_data)

    # print the certificate in human-readable format
    # Convert the certificate to a PEM-formatted string and print it
    # create an OpenSSL X509 object from the certificate data
    x509 = crypto.load_certificate(crypto.FILETYPE_PEM, cert_data)

    # print the certificate details
    print(f'Subject: {x509.get_subject()}')
    print(f'Serial Number: {x509.get_serial_number()}')
    print(f'Valid From: {datetime.strptime(x509.get_notBefore().decode("utf-8"), "%Y%m%d%H%M%SZ")}')
    print(f'Valid To: {datetime.strptime(x509.get_notAfter().decode("utf-8"), "%Y%m%d%H%M%SZ")}')
    print(f'Issuer: {x509.get_issuer()}')

    fileNameToWrite = "%s-%d" %("pkcs12File", time.time())

    #with open(csrKeyFileGenerated, "r") as src:
    #    csr_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
    csr_key = load_private_key(csrKeyFileGenerated)
    cert_client = load_certificate(cerFileGenerated)

    cp12FileDestination = os.path.join(certsRepo, fileNameToWrite + '.p12')    
    cleanFolderForFile(cp12FileDestination)

    export_to_pkcs12(cp12FileDestination,csr_key,cert_client,'passphrase','commonName0001' )

    print(f'p12 File:{cp12FileDestination} , exist?: {os.path.isfile(cp12FileDestination)}')

    aia = cert_client.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value
    ocsps = [ia for ia in aia if ia.access_method == AuthorityInformationAccessOID.OCSP]

    aia = cert_client.extensions.get_extension_for_oid(ExtensionOID.AUTHORITY_INFORMATION_ACCESS).value
    issuers = [ia for ia in aia if ia.access_method == AuthorityInformationAccessOID.CA_ISSUERS]

    if not issuers:
        raise Exception(f'no exist issuers entry in AIA')
    print(f'url issuer: {issuers[0].access_location.value}')
    if not ocsps:
        raise Exception(f'no exist ocsp entry in AIA')
    print(f'url ocsp: {ocsps[0].access_location.value}')

    logger.info("--------- Fin -----------------")


if __name__ == "__main__":
    print("Iniciando el Sistema...")

    logger.info("Inicializando Generate PKCS12 App")
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Saliendo de aplicación Generate PKCS12 App")
        sys.exit(0)
    except Exception as e:
        logger.error(f"Ha ocurrido un error inesperado: {e}")
        sys.exit(1)
