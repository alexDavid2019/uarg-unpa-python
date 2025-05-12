# coding: utf-8
from datetime import datetime
import os

import asn1crypto.x509
from oscrypto import asymmetric
from asn1crypto.util import timezone
from ocspbuilder import OCSPResponseBuilder

path_root = os.path.dirname(__file__)
certsRepo_dir = os.path.join(path_root, 'certsRepo')

class OCSPResponseBuilderTests():

    def test_build_good_response():
        #issuer_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'test.key'))
        #issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        #subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        issuer_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'caAutoSigned-1745188534.key'))
        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'caAutoSigned-1745188534.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'ocsp_certificateResponse-1745188535.cer'))

        builder = OCSPResponseBuilder('successful', subject_cert, 'good')
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        print(response_data)

        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        
        cert_response = response_data['responses'][0]

        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)
        #self.assertEqual('good', cert_response['cert_status'].name)
        #self.assertGreaterEqual(datetime.now(timezone.utc), cert_response['this_update'].native)
        return der_bytes
        
    def test_build_revoked_response():
        #issuer_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'test.key'))
        #issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        #subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        issuer_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'caAutoSigned-1745188534.key'))
        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'caAutoSigned-1745188534.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'ocsp_certificateResponse-1745188535.cer'))


        revoked_time = datetime(2015, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
        builder = OCSPResponseBuilder('successful', subject_cert, 'key_compromise', revoked_time)
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']
        print(response_data)
        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)

        #self.assertEqual('revoked', cert_response['cert_status'].name)
        #self.assertEqual(revoked_time, cert_response['cert_status'].chosen['revocation_time'].native)
        
        return der_bytes

    def test_build_revoked_no_reason():
        issuer_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'test.key'))
        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        revoked_time = datetime(2015, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
        builder = OCSPResponseBuilder('successful', subject_cert, 'revoked', revoked_time)
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        print(response_data)

        cert_response = response_data['responses'][0]

        #self.assertEqual('revoked', cert_response['cert_status'].name)
        #self.assertEqual(revoked_time, cert_response['cert_status'].chosen['revocation_time'].native)
        #self.assertEqual('unspecified', cert_response['cert_status'].chosen['revocation_reason'].native)

        return der_bytes
    
    def test_build_delegated_good_response():
        #responder_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'test-ocsp.key'), 'password')
        #responder_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-ocsp.crt'))
        #issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        #subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        responder_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'ocsp_certificateResponse-1745188535.key'))
        responder_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'ocsp_certificateResponse-1745188535.cer'))
        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'caAutoSigned-1745188534.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'ocsp_certificateResponse-1745188535.cer'))

        builder = OCSPResponseBuilder('successful', subject_cert, 'good')
        builder.certificate_issuer = issuer_cert
        ocsp_response = builder.build(responder_key, responder_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        print(response_data)
        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        
        cert_response = response_data['responses'][0]

        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)

        #self.assertEqual('good', cert_response['cert_status'].name)
        #self.assertGreaterEqual(datetime.now(timezone.utc), cert_response['this_update'].native)
        return der_bytes
        
    def test_build_unknown_response():
        issuer_key = asymmetric.load_private_key(os.path.join(certsRepo_dir, 'test.key'))
        issuer_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test.crt'))
        subject_cert = asymmetric.load_certificate(os.path.join(certsRepo_dir, 'test-inter.crt'))

        builder = OCSPResponseBuilder('successful', subject_cert, 'unknown')
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        print(response_data)
        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        
        cert_response = response_data['responses'][0]

        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)

        #self.assertEqual('unknown', cert_response['cert_status'].name)
        #self.assertGreaterEqual(datetime.now(timezone.utc), cert_response['this_update'].native)
        
        return der_bytes
    
    def test_build_error_response():
        """
        Build a response with error status.
        """
        error_statuses = ['malformed_request', 'internal_error',
                          'try_later', 'sign_required', 'unauthorized']

        for status in error_statuses:
            builder = OCSPResponseBuilder(status)
            ocsp_response = builder.build()
            der_bytes = ocsp_response.dump()

            new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
            assert dict(new_response.native) == {
                'response_status': status,
                'response_bytes': None,
            }
