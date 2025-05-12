from OpenSSL import crypto

from cryptography import x509
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.serialization import pkcs12, PrivateFormat
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from cryptography.hazmat.primitives.asymmetric import padding
import base64


def get_serial_number_of_cert(cert):
    '''Returns cert.serial_number.
    Also works for old versions of cryptography.
    '''
    try:
        return cert.serial_number
    except AttributeError:
        # The property was called "serial" before cryptography 1.4
        return cert.serial

def get_random_serial_number():
    return x509.random_serial_number()

def sign_message(message, pkPemFilePath, passwordPemFile=None):
    bytes_pem_private_key = open(pkPemFilePath).read().encode('UTF-8')

    if (passwordPemFile==None):
        private_key = serialization.load_pem_private_key(
                bytes_pem_private_key,
                password=None,
                backend=default_backend()
        )
    else:
        private_key = serialization.load_pem_private_key(
                bytes_pem_private_key,
                password=passwordPemFile.encode('UTF-8'),
                backend=default_backend()
        )
    
    signature = private_key.sign(
        message,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )
    return base64.b64encode(signature).decode()

def export_to_pkcs12(filename, private_key, cert, passphrase=None, commonName=None):
    #Ha ocurrido un error inesperado: module 'OpenSSL.crypto' has no attribute 'PKCS12'
    #pkcs = crypto.PKCS12()
    #pkcs.set_privatekey(private_key)
    #pkcs.set_certificate(cert)
    #pkcs.set_ca_certificates(_load_certs(chain_path))
    #with open(filename, 'wb') as file:
    #    file.write(pkcs.export(passphrase=passphrase))

    if private_key is not None and not isinstance(private_key,(rsa.RSAPrivateKey),):
        raise TypeError( "private_key must be RSA instances of RSAPrivateKey or None."
        )

    encryption = (
        PrivateFormat.PKCS12.encryption_builder().
        kdf_rounds(50000).
        key_cert_algorithm(pkcs12.PBES.PBESv2SHA256AndAES256CBC).
        hmac_hash(hashes.SHA512()).
        build(f"{passphrase}".encode())
    )

    p12 = pkcs12.serialize_key_and_certificates(
        f"{commonName}".encode(), private_key, cert, None, encryption
    )
    with open(filename, "wb") as file:  # .p12 and .pfx are the same
        file.write(p12)
    

def pem_to_x509(cert_data: str):
    """Converts a given pem encoded certificate to X509 object
    @param cert_data: str pem encoded certificate data that includes the header and footer
    @return: X509 object
    """
    return crypto.load_certificate(crypto.FILETYPE_PEM, str.encode(cert_data)) 


def _cryptography_get_keyusage(usage):
    '''
    Given a key usage identifier string, returns the parameter name used by cryptography's x509.KeyUsage().
    Raises an OpenSSLObjectError if the identifier is unknown.
    '''
    if usage in ('Digital Signature', 'digitalSignature'):
        return 'digital_signature'
    if usage in ('Non Repudiation', 'nonRepudiation'):
        return 'content_commitment'
    if usage in ('Key Encipherment', 'keyEncipherment'):
        return 'key_encipherment'
    if usage in ('Data Encipherment', 'dataEncipherment'):
        return 'data_encipherment'
    if usage in ('Key Agreement', 'keyAgreement'):
        return 'key_agreement'
    if usage in ('Certificate Sign', 'keyCertSign'):
        return 'key_cert_sign'
    if usage in ('CRL Sign', 'cRLSign'):
        return 'crl_sign'
    if usage in ('Encipher Only', 'encipherOnly'):
        return 'encipher_only'
    if usage in ('Decipher Only', 'decipherOnly'):
        return 'decipher_only'


def cryptography_parse_key_usage_params(usages):
    '''
    Given a list of key usage identifier strings, returns the parameters for cryptography's x509.KeyUsage().
    Raises an OpenSSLObjectError if an identifier is unknown.
    '''
    params = dict(
        digital_signature=False,
        content_commitment=False,
        key_encipherment=False,
        data_encipherment=False,
        key_agreement=False,
        key_cert_sign=False,
        crl_sign=False,
        encipher_only=False,
        decipher_only=False,
    )
    for usage in usages:
        params[_cryptography_get_keyusage(usage)] = True
    return params


def generate_rsa_key():
    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    return private_key

def save_rsa_key(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as pem_out:
        pem_out.write(pem)


def save_key_bad(pk, filename):
    pem = pk.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.TraditionalOpenSSL,
        encryption_algorithm=serialization.NoEncryption()
    )
    pem_data = pem.splitlines()
    with open(filename, 'wb') as pem_out:
        for line in pem_data:
            pem_out.write(line)


def load_private_key(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    private_key = load_pem_private_key(pemlines, None, default_backend())
    return private_key

def load_certificate(filename):
    with open(filename, 'rb') as pem_in:
        pemlines = pem_in.read()
    _cert = x509.load_pem_x509_certificate(pemlines, default_backend())
    return _cert
