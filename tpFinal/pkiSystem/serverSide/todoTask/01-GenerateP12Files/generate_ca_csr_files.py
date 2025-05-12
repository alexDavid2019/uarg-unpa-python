"""
Recomendaciones para el orden de importacion:
"""
#1. Librerias standard
import sys
import time 
import os
import random
#2. Librerias de terceros
#!pip install pyOpenSSL
from OpenSSL import crypto
from cryptography.x509 import load_der_x509_certificate

#3. Librerias propias
from custom_fileIO import writeFile,cleanFolderForFile
from custom_certUtil import pem_to_x509

county = "AR"
state = "Buenos Aires"
city = "CABA"

ca_name_organization = "Infraestructura de Firma Digital de la República Argentina"
ca_name_department = "Infraestructura de Firma Digital"

key_length_RSA = 4096
hash_algorithm = "sha512" 

def getGenerateCA(pathRoot="folder", fileNameToWrite='test', commonNameCA=''):
    ## Generate private key using OPENSSL
    # create a key pair
    private_key = crypto.PKey()
    private_key.generate_key(crypto.TYPE_RSA, key_length_RSA)

    print("--- create CA Cert -----")
    # Create a CA certificate
    cert_ca = crypto.X509()
    cert_ca.get_subject().commonName = commonNameCA
    cert_ca.get_subject().countryName = county 
    cert_ca.get_subject().stateOrProvinceName = state 
    cert_ca.get_subject().localityName = city 
    cert_ca.get_subject().organizationName = ca_name_organization 
    cert_ca.get_subject().organizationalUnitName = ca_name_department
    cert_ca.get_subject().emailAddress = "test@domain.com"

    cert_ca.add_extensions([
        crypto.X509Extension(b"basicConstraints", True, b"CA:TRUE, pathlen:0"),
        crypto.X509Extension(b"keyUsage", False, b"keyCertSign, cRLSign"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=cert_ca),
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid,issuer",issuer=cert_ca),
    ])

    # Generate a random serial number
    cert_ca.set_serial_number(random.getrandbits(128))
    # Set the certificate version to 2, which supports X509 extensions.
    cert_ca.set_version(2)  # 0 = version '1', 1 = version '2', 2 = version '3'.
    cert_ca.gmtime_adj_notBefore(0)
    # CA: 10 years should be enough for everyone
    cert_ca.gmtime_adj_notAfter(10 * 365 * 24 * 60 * 60)

    cert_ca.set_issuer(cert_ca.get_subject())
    cert_ca.set_pubkey(private_key)
    cert_ca.sign(private_key, hash_algorithm)

    print("--- save CA Cert as pem file -----")
 
    caFileDestination = os.path.join(pathRoot, fileNameToWrite + '.crt')    
    cleanFolderForFile(caFileDestination)

    caKeyFileDestination = os.path.join(pathRoot, fileNameToWrite + '.key')    
    cleanFolderForFile(caKeyFileDestination)
    
    # Write the certificate and key back to disk.
    writeFile(caFileDestination, crypto.dump_certificate(crypto.FILETYPE_PEM, cert_ca))
    writeFile(caKeyFileDestination, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
    print("--- Finished. CA Cert generated -----")
    return caFileDestination,caKeyFileDestination 


def getGenerateCSRSigned(pathRoot="folder", fileNameToWrite='test', pemFileCA='',csr_common_name='', csr_name_organization='', csr_name_department=''):

    ## Generate private key using OPENSSL
    # create a key pair
    private_key = crypto.PKey()
    private_key.generate_key(crypto.TYPE_RSA, key_length_RSA)

    print("Read CA pem file...")
    with open(pemFileCA, "r") as src:
        cert_ca = pem_to_x509(src.read()) 

    print("--- create our CRS Req -----")

     # creaing the CRS request
    csr_req = crypto.X509Req()

    csr_req.get_subject().commonName = csr_common_name
    csr_req.get_subject().countryName = county 
    csr_req.get_subject().stateOrProvinceName = state 
    csr_req.get_subject().localityName = city 
    csr_req.get_subject().organizationName = csr_name_organization 
    csr_req.get_subject().organizationalUnitName = csr_name_department
    csr_req.get_subject().emailAddress = "csr@domain.com"
    
    csr_req.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE, pathlen:0"),
        crypto.X509Extension(b"keyUsage", False, b"digitalSignature, keyCertSign, cRLSign"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=cert_ca),
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid,issuer",issuer=cert_ca),
    ])

    csr_req.set_pubkey(private_key)
    csr_req.sign(private_key, hash_algorithm)

    print("--- save CSR Req as pem file -----")

    csrFileDestination = os.path.join(pathRoot, fileNameToWrite + '.csr')    
    cleanFolderForFile(csrFileDestination)

    csrKeyFileDestination = os.path.join(pathRoot, fileNameToWrite + '.key')    
    cleanFolderForFile(csrKeyFileDestination)

    # Write the certificate and key back to disk.
    writeFile(csrFileDestination, crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr_req))
    writeFile(csrKeyFileDestination, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
    print("--- Finished. CSR generated -----")
    return csrFileDestination,csrKeyFileDestination
    