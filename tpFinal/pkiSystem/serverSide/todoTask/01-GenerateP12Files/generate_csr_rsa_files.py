"""
Recomendaciones para el orden de importacion:
"""
#1. Librerias standard
import sys
import time 
import os
import argparse
#2. Librerias de terceros
from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.x509.oid import NameOID
#3. Librerias propias
from custom_fileIO import cleanFolderForFile

# Ver https://cryptography.readthedocs.org/en/latest/x509/tutorial/
# Ver https://cryptography.io/en/latest/x509/reference/#cryptography.x509.CertificateSigningRequestBuilder

county = "AR"
state = "Buenos Aires"
city = "CABA"
name_organization = "Infraestructura de Firma Digital de la República Argentina"
name_department = "Infraestructura de Firma Digital"
key_length_RSA = 4096

def getGenerateCSRSigned(pathRoot="folder", partFileName='test', commonNameCsr=''):

    ## Generate private key using RSA cryptography
    # create a key pair
    private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=key_length_RSA,
            backend=default_backend()
        )

    builder = x509.CertificateSigningRequestBuilder()

    # Generate a CSR
    builder = builder.subject_name(x509.Name([
            x509.NameAttribute(NameOID.COUNTRY_NAME, county),
            x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, state),
            x509.NameAttribute(NameOID.LOCALITY_NAME, city),
            x509.NameAttribute(NameOID.ORGANIZATION_NAME, name_organization),
            x509.NameAttribute(NameOID.COMMON_NAME, commonNameCsr),
            ]))
    builder = builder.add_extension(x509.SubjectAlternativeName([
                x509.DNSName("mysite.com"),
                x509.DNSName("www.mysite.com"),
                x509.DNSName("subdomain.mysite.com"),
            ]),critical=False)
    builder = builder.add_extension(x509.BasicConstraints(ca=False, path_length=None),critical=False)

    print("Sign the CSR with our private key...")
    # Sign the CSR with our private key.
    kx_csr = builder.sign(private_key, hashes.SHA512(), default_backend())
    
    print("Write files whith our private key...")

    #Guardamos la key en formato accesible por openSSl sin encriptacion.
    #privateKey_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,  
    #                format=serialization.PrivateFormat.PKCS8,  
    #                encryption_algorithm=serialization.NoEncryption())  
    privateKey_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,  
                    format=serialization.PrivateFormat.TraditionalOpenSSL,  
                    encryption_algorithm=serialization.NoEncryption())  
    
    fileFolderDestination = os.path.join(pathRoot, partFileName + '.key')    
    cleanFolderForFile(fileFolderDestination)
    with open(fileFolderDestination, 'wb') as f :
        os.fchmod(f.fileno(), 0o400)
        f.write(privateKey_pem)

    public_key = private_key.public_key()  
    publicKey_pem = public_key.public_bytes(  
        encoding=serialization.Encoding.PEM,  
        format=serialization.PublicFormat.SubjectPublicKeyInfo      
    )
    
    fileFolderDestination = os.path.join(pathRoot, partFileName + '.pub')
    cleanFolderForFile(fileFolderDestination)
    # Write our public key to disk.
    with open(fileFolderDestination, 'wb') as f :
        f.write(publicKey_pem)
    
    pemSigned = kx_csr.public_bytes(serialization.Encoding.PEM)

    fileFolderDestination = os.path.join(pathRoot, partFileName + '.csr')
    cleanFolderForFile(fileFolderDestination)
    # Write our CSR signed to disk.
    with open(fileFolderDestination, 'wb') as f :
        f.write(pemSigned)
    