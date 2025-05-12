#1. Librerias standard
import time 
import os
import random
from datetime import datetime, timedelta
from tzlocal import get_localzone # pip install tzlocal
#2. Librerias de terceros

#!pip install pyOpenSSL
from OpenSSL import crypto

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
#from cryptography.x509 import (CertificateRevocationList, RevokedCertificate, )
from cryptography.x509.oid import (AuthorityInformationAccessOID, NameOID, SignatureAlgorithmOID, )


from pyhanko.pdf_utils import text, images
from pyhanko.pdf_utils.incremental_writer import IncrementalPdfFileWriter
from pyhanko.sign import signers, timestamps, fields
from pyhanko.sign.fields import SigSeedSubFilter
from pyhanko_certvalidator import ValidationContext
from pyhanko import stamp

#3. Librerias propias
import lib.global_variable as glv
from lib.custom_fileIO import *
from lib.custom_certUtil import *
from lib.constants import *

class X509Key(object):
    """Representation of a private key
    Without any arguments this class just creates an empty instance. Provide a
    PEM encoded private key and it will load and decrypt it (if ``password`` is provided as well).
    Args:
        pem (:obj:`bytes`, optional): The PEM encoded private key
        password (:obj:`str`, optional): Password in case the PEM is enrypted
        backend (:obj:`backend`, optional): Specify a backend to use
    """
    def __init__(self, pem=None, password=None, backend=default_backend):
        if pem:
            self.key = serialization.load_pem_private_key(pem, password=password, backend=backend())

    @property
    def pem(self) -> bytes:
        """bytes: Return PEM encoded unencryped key"""
        return self.key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        )

    #class ToString()
    def __str__(self):
        r = self.pem
        return '\n'.join(r)

class X509Cert(object):
    """Representation of a X509 Certificate

    Without any arguments this class just creates an empty instance. Provide a
    PEM encoded Certificate and it will load and it.

    Args:
        pem (:obj:`bytes`, optional): The PEM encoded Certificate
        backend (:obj:`backend`, optional): Specify a backend to use
    """

    def __init__(self, cert=None, backend=default_backend):
        if cert:
            self.cert = x509.load_pem_x509_certificate(cert, backend=backend())
    
    @property
    def pem(self) -> bytes:
        """bytes: PEM encoded Certificate"""
        return self.cert.public_bytes(encoding=serialization.Encoding.PEM,)
    
    #class ToString()
    def __str__(self):
        r = self.pem
        return '\n'.join(r)


class CRLCert(object):
    """Representation of a CRL Certificate

    Without any arguments this class just creates an empty instance. Provide a
    PEM encoded Certificate and it will load and it.

    Args:
        pem (:obj:`bytes`, optional): The PEM encoded Certificate
        backend (:obj:`backend`, optional): Specify a backend to use
    """

    def __init__(self, crlData=None, backend=default_backend):
        if crlData:
            #self.cert = x509.load_pem_x509_crl(crlData, backend=backend())
            self.cert = x509.load_der_x509_crl(crlData, backend=backend())
    
    @property
    def pem(self) -> bytes:
        """bytes: PEM/DER encoded Certificate"""
        #return self.cert.public_bytes(encoding=serialization.Encoding.PEM, )
        return self.cert.public_bytes(encoding=serialization.Encoding.DER, )

    #class ToString()
    def __str__(self):
        r = self.pem
        return '\n'.join(r)


class CertificateAuthority(object):

    def __init__(self, key_pem, cert_pem):
        self.key = None
        self.cert = X509Cert(cert_pem)
        if (key_pem is not None):
            self.key = X509Key(key_pem)


class CrlCertificate(object):

    def __init__(self, cert_pem):
        self.cert = CRLCert(cert_pem)


class CertificateDummy:

    #constructor
    #def __init__(self):
    #    algo .....

    #class ToString()
    def __str__(self):
        r = [URI_OCSP]
        r.append(URI_CA_CRT)
        r.append(URI_CRL)
        return '\n'.join(r)

    def getCertificates(self, path_dir) -> list:
        listFiles = get_files_recursive(path_dir)
        return listFiles

    def getMetadataFiles(self, path_dir) -> dict:
        metadata = get_files_recursive_metadata(path_dir)
        return metadata

    def generateCACertificate(self, pathRoot="folder", 
                              fileNameToWrite='ca', 
                              commonNameforOurCA='company'):
        ## Generate private and public key using OPENSSL
        private_key = crypto.PKey()
        private_key.generate_key(crypto.TYPE_RSA, KEY_LEN_RSA)

        # Create a CA certificate
        cert_ca = crypto.X509()
        cert_ca.get_subject().commonName = commonNameforOurCA
        cert_ca.get_subject().countryName = COUNTRY 
        cert_ca.get_subject().stateOrProvinceName = STATE 
        cert_ca.get_subject().localityName = CITY
        cert_ca.get_subject().organizationName = CA_ORGANIZATION_NAME 
        cert_ca.get_subject().organizationalUnitName = CA_DEPARMENT_NAME
        cert_ca.get_subject().emailAddress = "noreply@domain-ca.com"

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
        cert_ca.sign(private_key, HASH_ALGORITHM)

        caPathFile = os.path.join(pathRoot, fileNameToWrite + '.crt')    
        cleanFolderForFile(caPathFile)

        caKeyPathFile = os.path.join(pathRoot, fileNameToWrite + '.key')    
        cleanFolderForFile(caKeyPathFile)

        # Write the certificate and key back to disk.
        writeFile(caPathFile, crypto.dump_certificate(crypto.FILETYPE_PEM, cert_ca))
        writeFile(caKeyPathFile, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
        return caPathFile, caKeyPathFile 

    def generateCSRAutoSigned(self, pathRoot="folder", 
                              fileNameToWrite='test', 
                              pemFileCA='',
                              csr_common_name='', 
                              csr_name_organization='', 
                              csr_name_department='', csr_email=''):
        ## Generate private and public key using OPENSSL
        private_key = crypto.PKey()
        private_key.generate_key(crypto.TYPE_RSA, KEY_LEN_RSA)

        with open(pemFileCA, "r") as src:
            cert_ca = pem_to_x509(src.read()) 

        #creaing the CRS request
        csr_req = crypto.X509Req()

        csr_req.get_subject().commonName = csr_common_name
        csr_req.get_subject().countryName = COUNTRY 
        csr_req.get_subject().stateOrProvinceName = STATE 
        csr_req.get_subject().localityName = CITY 
        csr_req.get_subject().organizationName = csr_name_organization 
        csr_req.get_subject().organizationalUnitName = csr_name_department
        csr_req.get_subject().emailAddress = csr_email # "noreply@domain-csr.com"
        
        csr_req.add_extensions([
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE, pathlen:0"),
            crypto.X509Extension(b"keyUsage", False, b"digitalSignature, keyCertSign, cRLSign"),
            crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=cert_ca),
            crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid,issuer",issuer=cert_ca),
        ])

        csr_req.set_pubkey(private_key)
        csr_req.sign(private_key, HASH_ALGORITHM)

        csrPathFile = os.path.join(pathRoot, fileNameToWrite + '.csr')    
        cleanFolderForFile(csrPathFile)

        csrKeyPathFile = os.path.join(pathRoot, fileNameToWrite + '.key')    
        cleanFolderForFile(csrKeyPathFile)

        # Write the certificate and key back to disk.
        writeFile(csrPathFile, crypto.dump_certificate_request(crypto.FILETYPE_PEM, csr_req))
        writeFile(csrKeyPathFile, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
        return csrPathFile,csrKeyPathFile


    def generateCertificate(self, pathRoot="folder", 
                            fileNameToWrite='test', 
                            commonNameCert = '', 
                            name_organization = '', 
                            name_department = '', 
                            email_Address = '', 
                            pemFileCA='', 
                            keyFileCA='', 
                            csrFile='', csrKeyFile=''):
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

        #print("1.Read CA file...")
        with open(pemFileCA, "r") as src:
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM,src.read())

        with open(keyFileCA, "r") as src:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
            
        #print("2.Read CSR file...")
        with open(csrKeyFile, "r") as src:
            csr_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
            
        with open(csrFile, "r") as src:
            csr_req = crypto.load_certificate_request(crypto.FILETYPE_PEM,src.read())


        certs = crypto.X509()
    
        certs.get_subject().commonName = commonNameCert
        certs.get_subject().countryName = COUNTRY 
        certs.get_subject().stateOrProvinceName = STATE 
        certs.get_subject().localityName = CITY 
        certs.get_subject().organizationName = name_organization 
        certs.get_subject().organizationalUnitName = name_department
        certs.get_subject().emailAddress = email_Address

        # Generate a random serial number
        # serial number reuse.
        certs.set_serial_number(random.getrandbits(128))
        #certs.set_serial_number(random.randint(50000000, 100000000))
        #certs.set_serial_number(int(time.time())) # or cert_serial_number
        # Set the certificate version to 2, which supports X509 extensions.
        certs.set_version(2)  # 0 = version 1, 1 = version 2, 2 = version 3.
        certs.gmtime_adj_notBefore(0)
        # 1 year  should be enough for everyone
        certs.gmtime_adj_notAfter(1 * 365 * 24 * 60 * 60)
        #certs.gmtime_adj_notAfter(datetime.datetime.today() + datetime.timedelta(days=365))

        certs.add_extensions([
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
        ])

        authorityInfoAccess = []
        authorityInfoAccess.append(f"OCSP;URI:{URI_OCSP}")
        authorityInfoAccess.append(f"caIssuers;URI:{URI_CA_CRT}")

        crlDistributionPoints_bytes = f"URI:{URI_CRL}".encode('utf-8')

        certs.add_extensions([
            crypto.X509Extension(b"extendedKeyUsage", False, b"codeSigning, clientAuth"),
            crypto.X509Extension(b"keyUsage", True, b"keyCertSign, cRLSign, digitalSignature, nonRepudiation, keyEncipherment, dataEncipherment"),
            crypto.X509Extension(b"crlDistributionPoints",False, crlDistributionPoints_bytes),
            crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=ca_cert),
            crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always,issuer:always",issuer=ca_cert),
        ])

        if len(authorityInfoAccess) > 0:
            authorityInfoAccess_b = bytes(",".join(authorityInfoAccess), 'utf-8')
            certs.add_extensions([
                crypto.X509Extension(b"authorityInfoAccess", False, authorityInfoAccess_b),
            ])

        certs.set_subject(csr_req.get_subject())
        #certs.set_issuer(ca_cert.get_subject())
        certs.set_pubkey(csr_key)
        certs.sign(ca_key, HASH_ALGORITHM)
        
        cerPathFile = os.path.join(pathRoot, fileNameToWrite + '.cer')    
        cleanFolderForFile(cerPathFile)
        
        # Write the certificate and key back to disk.
        writeFile(cerPathFile, crypto.dump_certificate(crypto.FILETYPE_PEM, certs))

        #Mergeamos el cer con el certificado CA en un nuevo archivo
        filesToMerge = [cerPathFile,pemFileCA]
        fileNameToWrite = "%s-%d" %("certificateWithCA", time.time())
        cerMerged = os.path.join(pathRoot, fileNameToWrite + '.cer')    
        with open(cerMerged, 'w') as outfile:
            for fname in filesToMerge:
                with open(fname) as infile:
                    for line in infile:
                        outfile.write(line)

        #borramos el cer sin el merge de la CA
        cleanFolderForFile(cerPathFile)
        #renombramos el archivo mergeado con el mismo nombre del archivo eliminado.
        os.rename(cerMerged, cerPathFile)
        return cerPathFile, certs.get_serial_number()


    def generateOcspResponseCertificate(self,
                                        pathRoot="folder", 
                                        fileNameToWrite='test', 
                                        commonNameCert = 'ocsp Response', 
                                        pemFileCA='', 
                                        keyFileCA=''):

        ## Generate private and public key using OPENSSL
        private_key = crypto.PKey()
        private_key.generate_key(crypto.TYPE_RSA, OCSP_KEY_LEN_RSA)
    
        #print("1.Read CA file...")
        with open(pemFileCA, "r") as src:
            ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM,src.read())

        with open(keyFileCA, "r") as src:
            ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())
                
        certs = crypto.X509()
    
        certs.get_subject().commonName = commonNameCert
        certs.get_subject().countryName = COUNTRY 
        certs.get_subject().stateOrProvinceName = STATE 
        certs.get_subject().localityName = CITY 
        certs.get_subject().organizationName = OCSP_ORGANIZATION_NAME 
        certs.get_subject().organizationalUnitName = OCSP_DEPARMENT_NAME
        certs.get_subject().emailAddress = "our_ocsp_cert_response@domain-ocsp.com"

        # Generate a random serial number
        # serial number reuse.
        certs.set_serial_number(random.getrandbits(128))
        #certs.set_serial_number(random.randint(50000000, 100000000))
        #certs.set_serial_number(int(time.time())) # or cert_serial_number
        # Set the certificate version to 2, which supports X509 extensions.
        certs.set_version(2)  # 0 = version 1, 1 = version 2, 2 = version 3.
        certs.gmtime_adj_notBefore(0)
        # 1 year  should be enough for everyone
        certs.gmtime_adj_notAfter(1 * 365 * 24 * 60 * 60)
        #certs.gmtime_adj_notAfter(datetime.datetime.today() + datetime.timedelta(days=365))

        certs.add_extensions([
            crypto.X509Extension(b"basicConstraints", False, b"CA:FALSE"),
            #crypto.X509Extension(b"extendedKeyUsage", False, b"digitalSignature, nonRepudiation"),
            #crypto.X509Extension(b"keyUsage", True, b"OCSPSigning"),
            crypto.X509Extension(b"subjectKeyIdentifier", False, b"hash", subject=ca_cert),
            crypto.X509Extension(b"authorityKeyIdentifier", False, b"keyid:always,issuer:always",issuer=ca_cert),        
        ])
        certs.add_extensions([
            crypto.X509Extension(b"extendedKeyUsage", False, b"OCSPSigning"),
            crypto.X509Extension(b"keyUsage", True, b"digitalSignature, nonRepudiation "),
        ])

        certs.set_issuer(ca_cert.get_subject())
        certs.set_pubkey(private_key)
        certs.sign(private_key, OCSP_HASH_ALGORITHM)

        cerPathFile = os.path.join(pathRoot, fileNameToWrite + '.cer')    
        cleanFolderForFile(cerPathFile)

        cerKeyPathFile = os.path.join(pathRoot, fileNameToWrite + '.key')    
        cleanFolderForFile(cerKeyPathFile)

        # Write the certificate and key back to disk.
        writeFile(cerPathFile, crypto.dump_certificate(crypto.FILETYPE_PEM, certs))
        writeFile(cerKeyPathFile, crypto.dump_privatekey(crypto.FILETYPE_PEM, private_key))
        
        return cerPathFile, cerKeyPathFile

    def generateCrlCertificate(self, pathRoot="folder", 
                                        fileNameToWrite='test', 
                                        pemFileCA='', 
                                        keyFileCA='', backend=default_backend):

        #print("1.Read CA file...")
        #with open(pemFileCA, "r") as src:
        #    ca_cert = crypto.load_certificate(crypto.FILETYPE_PEM,src.read())
        #with open(keyFileCA, "r") as src:
        #    ca_key = crypto.load_privatekey(crypto.FILETYPE_PEM,src.read())

        # Generate a private key for the CA
        ca_private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )
        
        """
        Generate a certificate revocation list (CRL).

        Returns: None
        """
        #AttributeError: module 'OpenSSL.crypto' has no attribute 'CRL'
        #crl = crypto.CRL()
        #crl.set_lastUpdate(datetime.utcnow())
        #crl.set_nextUpdate(datetime.utcnow() + + timedelta(days=1))
        # Creates the revoked objects
        #revoked1 = crypto.Revoked()
        #revoked1.set_serial(b"1")                 # certificate's serial number
        #revoked1.set_rev_date(b"20190601010101Z") # certificate's revocation date
        #revoked1.set_reason(b'keyCompromise')     # certificate's revocation reason
        #revoked2 = crypto.Revoked()
        #revoked2.set_serial(b"2")
        #revoked2.set_rev_date(b"20190601010101Z")
        #revoked2.set_reason(None)
        #revokedList = [revoked1, revoked2, ]
        #for revoked in revokedList:
        #    crl.add_revoked(revoked)
        #crl.sign(ca_cert.cert, ca_cert.key, b"sha256")
        
        # Create a CRL

        crl_number = x509.CRLNumber(1)

        builder = x509.CertificateRevocationListBuilder()
        builder = builder.issuer_name(
                x509.Name(
                    [
                        x509.NameAttribute(
                            NameOID.COMMON_NAME, "Nuestra CA"
                        )
                    ]
                )
            )

        builder = builder.last_update(datetime.datetime.utcnow())
        builder = builder.next_update(datetime.datetime.utcnow() + timedelta(days=1))
        builder = builder.add_extension(crl_number, False)

        # Revoke the certificate
        revoked_cert1 = (
            x509.RevokedCertificateBuilder()
            .serial_number(2)
            .revocation_date(datetime.datetime(2012, 1, 1, 1, 1))
            .add_extension(
                x509.CRLReason(x509.ReasonFlags.ca_compromise), False
            )
            .build(backend)
        )

        revoked_cert2 = (
            x509.RevokedCertificateBuilder()
            .serial_number(40)
            .revocation_date(datetime.datetime.now(datetime.timezone.utc).replace(
                        tzinfo=None
                    )
            )
            .add_extension(
                x509.CRLReason(x509.ReasonFlags.ca_compromise), False
            )
            .build(backend)
        )
        builder = builder.add_revoked_certificate(revoked_cert1)
        builder = builder.add_revoked_certificate(revoked_cert2)

        # Sign the CRL
        crl = builder.sign(private_key=ca_private_key, 
                           algorithm=hashes.SHA256(), 
                           backend=default_backend)

        crlPathFile = os.path.join(pathRoot, fileNameToWrite + '.crl')    
        cleanFolderForFile(crlPathFile)

        # Write the certificate.
        #writeFile(crlPathFile, crl.public_bytes(serialization.Encoding.PEM))
        writeFile(crlPathFile, crl.public_bytes(serialization.Encoding.DER))
        
        return crlPathFile


    def signPdfWithPKCS12(pathRoot="folder", pcks12FileName='',password='',
                            pdfInputPathFile='', pdfOuputFileName=''):
        
        pcks12PathFile = os.path.join(pathRoot, pcks12FileName)    
        
        pdfOuputPathFile = os.path.join(pathRoot, pdfOuputFileName)
        
        cleanFolderForFile(pdfOuputPathFile)
        
        _sig_field_name = "Signature"
        # Load signer key material from PKCS#12 file
        # This assumes that any relevant intermediate certs are also included
        # in the PKCS#12 file.
        bytes_password = password.encode('utf-8')
        signer = signers.SimpleSigner.load_pkcs12(
            pfx_file=pcks12PathFile, passphrase=bytes_password
        )

        # Set up a timestamping client to fetch timestamps tokens
        #timestamper = timestamps.HTTPTimeStamper(
        #    url='http://tsa.example.com/timestampService'
        #)
        #https://gist.github.com/deeplook/130983de7220fdd64b35d0a76f53854d
        timestamp = datetime.datetime.now(tz=get_localzone())

        #Meta simple solo con el nombre
        signature_meta = signers.PdfSignatureMetadata(
        #                location='xxxxx', 
        #                contact_info='xxxxxxxx',
        #                name='xxxxxxx',
                        certify=True,
                        field_name=_sig_field_name, 
                        md_algorithm='sha256',
                        # Tell pyHanko to put in an extra DocumentTimeStamp
                        # to kick off the PAdES-LTA timestamp chain.
                        use_pades_lta=True
                        )

        #Meta que permite validar ocsp y crl al momento de firmar
        #signature_meta = signers.PdfSignatureMetadata(
        #    field_name=_sig_field_name, 
        #    md_algorithm='sha256',
        #    # Mark the signature as a PAdES signature
        #    subfilter=SigSeedSubFilter.PADES,
        #    # We'll also need a validation context to fetch & embed revocation info.
        #    validation_context=ValidationContext(allow_fetching=True),
        #    # Embed relevant OCSP responses / CRLs (PAdES-LT)
        #    embed_validation_info=True,
        #    # Tell pyHanko to put in an extra DocumentTimeStamp
        #    # to kick off the PAdES-LTA timestamp chain.
        #    use_pades_lta=True
        #)

        #numeracion inversa en negativo. -1 ultima pagina, -2 ante ultima. 0 primera pagina.
        PAGE = -1
        # Specify the position and size of the stamp
        left = 100  # x coordinate of the lower left corner in points
        bottom = 100  # y coordinate of the lower left corner in points
        right = 200  # x coordinate of the upper right corner in points
        top = 200  # y coordinate of the upper right corner in points
        #box=(200, 600, 400, 660)
        
        if (os.path.exists(pdfInputPathFile) is False):
            raise Exception(f"Archivo no existe:{pdfInputPathFile}.")
        
        _sig_field_spec=fields.SigFieldSpec(
            sig_field_name=_sig_field_name,
            empty_field_appearance=True,
            readable_field_name="Test test",
        )

        _sig_field_spec=fields.SigFieldSpec(
                    sig_field_name=_sig_field_name,
                    on_page=PAGE, 
                    box=(left, bottom, right, top)
        )

        with open(pdfInputPathFile, 'rb') as inf:
            w = IncrementalPdfFileWriter(inf)
            fields.append_signature_field(w,sig_field_spec=_sig_field_spec)

            #Especificacion sin stamp de firma
            #pdf_signer = signers.PdfSigner(
            #    signature_meta, signer=signer, new_field_spec=_sig_field_spec
            #)
            #Especificacion con stamp y fondo de firma
            pdf_signer = signers.PdfSigner(
                signature_meta, signer=signer, stamp_style=stamp.TextStampStyle(
                    # the 'signer' and 'ts' parameters will be interpolated by pyHanko, if present
                    stamp_text='Signed by: %(signer)s\nTime: %(ts)s',
                    # background=images.PdfImage('stamp.png')
                ),
            )
            
            with open(pdfOuputPathFile, 'wb') as outf:
                pdf_signer.sign_pdf(w, output=outf)
                #signers.async_sign_pdf(w, output=outf)

        #time.sleep(5)  # Wait for 5 seconds

        if (os.path.exists(pdfOuputPathFile) is False):
            raise Exception(f"Archivo no existe:{pdfOuputPathFile}.")
        
        return pdfOuputPathFile

    def generatePkcs12Certificate(self, pathRoot="folder", 
                                  fileNameToWrite='test', 
                                  commonNameCert = 'localhost', 
                                  passwordPkcs12='1234', 
                                  cerPathFileGenerated='', 
                                  csrKeyFileGenerated=''):
        
        csr_private_key = load_private_key(csrKeyFileGenerated)
        cert_client = load_certificate(cerPathFileGenerated)

        p12PathFile = os.path.join(pathRoot, fileNameToWrite + '.p12')    
        cleanFolderForFile(p12PathFile)
        
        export_to_pkcs12(p12PathFile, csr_private_key, cert_client, passwordPkcs12, commonNameCert)
        
        return p12PathFile

    def saveDocumentOnDisk(self, pathRoot="folder", fileNameToWrite='test', base64Content=''):
        pdfPathFile = os.path.join(pathRoot, fileNameToWrite + '.pdf')    
        cleanFolderForFile(pdfPathFile)
        save_base64_to_pdf(base64Content, pdfPathFile)
        return pdfPathFile
    
    def getDocumentAsBase64(pathFile):
        return file_to_base64(pathFile)

    def getCertificateAuthority(publicPemFile, privatePemFile):
        key_pem = None
        cert_pem = None
        
        with open(publicPemFile,'rb') as fh:
            cert_pem = fh.read()
       
        if (privatePemFile is not None):
            with open(privatePemFile,'rb') as fh:
                key_pem = fh.read()
 
        return CertificateAuthority(key_pem, cert_pem)

    def getCRLCertificate(publicPemFile):
        with open(publicPemFile,'rb') as fh:
            cert_pem = fh.read()

        return CrlCertificate(cert_pem)
