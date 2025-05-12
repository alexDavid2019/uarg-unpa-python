import os

import asn1crypto.x509
from oscrypto import asymmetric
from ocspbuilder import OCSPRequestBuilder

path_root = os.path.dirname(__file__)
certsRepo_dir = os.path.join(path_root, 'certsRepo')


class OCSPRequestBuilderTests():

    def test_build_basic_request():
        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        builder = OCSPRequestBuilder(subject_cert, issuer_cert)
        ocsp_request = builder.build()
        der_bytes = ocsp_request.dump()

        new_request = asn1crypto.ocsp.OCSPRequest.load(der_bytes)
        tbs_request = new_request['tbs_request']

        print(tbs_request)

        request = tbs_request['request_list'][0]

        extn = tbs_request['request_extensions'][0]

        print(extn)

    def test_build_signed_request():

        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        requestor_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-third.crt'))
        requestor_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'test-third.key'))

        builder = OCSPRequestBuilder(subject_cert, issuer_cert)
        
        ocsp_request = builder.build(requestor_key, requestor_cert, [subject_cert, issuer_cert])
        der_bytes = ocsp_request.dump()

        new_request = asn1crypto.ocsp.OCSPRequest.load(der_bytes)
        tbs_request = new_request['tbs_request']
        
        print(tbs_request)

        signature = new_request['optional_signature']
        request = tbs_request['request_list'][0]
        
        