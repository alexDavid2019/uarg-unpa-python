"""
Recomendaciones para el orden de importacion:
"""
#1. Librerias standard
import sys
import time 
import datetime
import os
import random
#2. Librerias de terceros
#!pip install pyOpenSSL
from OpenSSL import crypto
from cryptography.hazmat.primitives.asymmetric import rsa

#3. Librerias propias
from custom_fileIO import writeFile,cleanFolderForFile

county = "AR"
state = "Buenos Aires"
city = "CABA"
name_organization = "Local OU"
name_department = "Firma Digital"
key_length_RSA = 4096
hash_algorithm = "sha512" 

ocsp_name_organization = "Local OCSP"
ocsp_name_department = "OCSP Signing Certificate Request"
ocsp_key_length_RSA = 2048
ocsp_hash_algorithm = "sha256" 

def getGenerateCertificate(pathRoot="folder", fileNameToWrite='test', commonNameCert = '', pemFileCA='', keyFileCA='', csrFile='', csrKeyFile=''):

    """
    Generate a certificate given a certificate request.
    Arguments: issuerName - The name of the issuer
               issuerKey  - The private key of the issuer
               serial     - Serial number for the certificate
               notBefore  - Timestamp (relative to now) when the certificate
                            starts being valid
               notAfter   - Timestamp (relative to now) when the certificate
                            stops being valid
               altNames   - The alternative names
               digest     - Digest method to use for signing, default is sha256
    Returns:   The signed certificate in an X509 object
    """

    print("--- create Client Cert -----")

    print("1.Read CA file...")
    with open(pemFileCA, "r") as src:
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM,src.read())

    with open(keyFileCA, "r") as src:
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
        
    print("2.Read CSR file...")
    with open(csrKeyFile, "r") as src:
        csr_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
        
    with open(csrFile, "r") as src:
        csr_req = crypto.load_certificate_request(crypto.FILETYPE_PEM,src.read())


    certs = crypto.X509()
  
    certs.get_subject().commonName = commonNameCert
    certs.get_subject().countryName = county 
    certs.get_subject().stateOrProvinceName = state 
    certs.get_subject().localityName = city 
    certs.get_subject().organizationName = name_organization 
    certs.get_subject().organizationalUnitName = name_department
    certs.get_subject().emailAddress = "our_cert_client@domain.com"

    # Generate a random serial number
    # serial number reuse.
    certs.set_serial_number(random.getrandbits(128))
    #certs.set_serial_number(random.randint(50000000, 100000000))
    #certs.set_serial_number(int(time.time())) # or cert_serial_number
    # Set the certificate version to 2, which supports X509 extensions.
    certs.set_version(2)  # 0 = version 1, 1 = version, 2 = version 3.
    certs.gmtime_adj_notBefore(0)
    # 1 year  should be enough for everyone
    certs.gmtime_adj_notAfter(1 * 365 * 24 * 60 * 60)
    #certs.gmtime_adj_notAfter(datetime.datetime.today() + datetime.timedelta(days=365))

    certs.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
    ])

    authorityInfoAccess = []
    authorityInfoAccess.append("OCSP;URI:http://localhost:8080/ocsp")
    authorityInfoAccess.append("caIssuers;URI:http://localhost:8080/ca.crt")

    certs.add_extensions([
        crypto.X509Extension(b"extendedKeyUsage", False, b"codeSigning, clientAuth"),
        crypto.X509Extension(b"keyUsage", True, b"keyCertSign, cRLSign, digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment"),
        crypto.X509Extension(b"crlDistributionPoints",False, b"URI:http://localhost:8080/crl"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=ca_cert),
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always,issuer:always",issuer=ca_cert),
    ])

    if len(authorityInfoAccess) > 0:
        authorityInfoAccess_b = bytes(",".join(authorityInfoAccess), 'utf-8')
        certs.add_extensions([
            crypto.X509Extension(b"authorityInfoAccess", False, authorityInfoAccess_b),
        ])

    #certs.set_subject(csr_req.get_subject())
    certs.set_issuer(ca_cert.get_subject())
    certs.set_pubkey(csr_key)
    certs.sign(ca_key, hash_algorithm)
    
    cerFile = os.path.join(pathRoot, fileNameToWrite + '.cer')    
    cleanFolderForFile(cerFile)

    #cerKeyFile = os.path.join(pathRoot, fileNameToWrite + '.key')    
    #cleanFolderForFile(cerKeyFile)
    
    # Write the certificate and key back to disk.
    writeFile(cerFile, crypto.dump_certificate(crypto.FILETYPE_PEM, certs))
    #writeFile(cerKeyFile, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
    print("--- Finished. Client Certificate generated -----")

    filesToMerge = [cerFile,pemFileCA]
    fileNameToWrite = "%s-%d" %("certificateWithCA", time.time())
    cerMerged = os.path.join(pathRoot, fileNameToWrite + '.cer')    
    with open(cerMerged, 'w') as outfile:
        for fname in filesToMerge:
            with open(fname) as infile:
                for line in infile:
                    outfile.write(line)
   
    return cerFile, cerMerged


def getGenerateOcspResponseCertificate(pathRoot="folder", fileNameToWrite='test', commonNameCert = 'ocsp Response', pemFileCA='', keyFileCA=''):

    ## Generate private key using OPENSSL
    # create a key pair
    private_key = crypto.PKey()
    private_key.generate_key(crypto.TYPE_RSA, ocsp_key_length_RSA)
  
    print("--- create OCSP Cert -----")

 
    print("1.Read CA file...")
    with open(pemFileCA, "r") as src:
        ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM,src.read())

    with open(keyFileCA, "r") as src:
        ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
               
    certs = crypto.X509()
  
    certs.get_subject().commonName = commonNameCert
    certs.get_subject().countryName = county 
    certs.get_subject().stateOrProvinceName = state 
    certs.get_subject().localityName = city 
    certs.get_subject().organizationName = ocsp_name_organization 
    certs.get_subject().organizationalUnitName = ocsp_name_department
    certs.get_subject().emailAddress = "our_ocsp_cert_response@domain.com"

    # Generate a random serial number
    # serial number reuse.
    certs.set_serial_number(random.getrandbits(128))
    #certs.set_serial_number(random.randint(50000000, 100000000))
    #certs.set_serial_number(int(time.time())) # or cert_serial_number
    # Set the certificate version to 2, which supports X509 extensions.
    certs.set_version(2)  # 0 = version 1, 1 = version, 2 = version 3.
    certs.gmtime_adj_notBefore(0)
    # 1 year  should be enough for everyone
    certs.gmtime_adj_notAfter(1 * 365 * 24 * 60 * 60)
    #certs.gmtime_adj_notAfter(datetime.datetime.today() + datetime.timedelta(days=365))

    certs.add_extensions([
        crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
    ])

    certs.add_extensions([
        crypto.X509Extension(b"extendedKeyUsage", False, b"OCSPSigning"),
        crypto.X509Extension(b"keyUsage", True, b"digitalSignature"),
        crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=ca_cert),
        crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always,issuer:always",issuer=ca_cert),        
    ])

    certs.set_issuer(ca_cert.get_subject())
    certs.set_pubkey(private_key)
    certs.sign(private_key, ocsp_hash_algorithm)
    
    cerFile = os.path.join(pathRoot, fileNameToWrite + '.cer')    
    cleanFolderForFile(cerFile)

    cerKeyFile = os.path.join(pathRoot, fileNameToWrite + '.key')    
    cleanFolderForFile(cerKeyFile)

    # Write the certificate and key back to disk.
    writeFile(cerFile, crypto.dump_certificate(crypto.FILETYPE_PEM, certs))
    writeFile(cerKeyFile, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
    print("--- Finished. OCSP Certificate generated -----")
    
    return cerFile, cerKeyFile
