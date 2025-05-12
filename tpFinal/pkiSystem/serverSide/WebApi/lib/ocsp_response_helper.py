# coding: utf-8
from datetime import datetime
import os
import sys
import asn1crypto.x509
from oscrypto import asymmetric
from asn1crypto.util import timezone
from lib.ocspbuilder import OCSPResponseBuilder
import lib.dbcontent as dbcontent
import lib.global_variable as glv

class OCSPResponseBuilderTests(object):

    def test_build_good_response(self):
        
        self.__base_path = glv.get_variable("FILES_REPO_DIR")
        if (self.__base_path == "Not Found"):
            sys.exit('global variable {}, is empty: {}'.format("FILES_REPO_DIR", self.__base_path))       

        self.__ca_list = dbcontent.certificate_ca_list()
        self.__ocsp_list = dbcontent.certificate_ocsp_list()
        
        ocsp_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ocsp_list))
        ca_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ca_list))
        ca_Key = list(filter(lambda c: c["iskey"] == "1", self.__ca_list))
        
        issuer_key = asymmetric.load_private_key(os.path.join(self.__base_path, ca_Key[0]["filename"]))
        issuer_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ca_NoKey[0]["filename"]))
        subject_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ocsp_NoKey[0]["filename"]))

        builder = OCSPResponseBuilder('successful', subject_cert, 'good')
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        #print(response_data)

        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        
        cert_response = response_data['responses'][0]

        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)
        #self.assertEqual('good', cert_response['cert_status'].name)
        #self.assertGreaterEqual(datetime.now(timezone.utc), cert_response['this_update'].native)
        return der_bytes
        
    def test_build_revoked_response(self):

        self.__base_path = glv.get_variable("FILES_REPO_DIR")
        if (self.__base_path == "Not Found"):
            sys.exit('global variable {}, is empty: {}'.format("FILES_REPO_DIR", self.__base_path))       

        self.__ca_list = dbcontent.certificate_ca_list()
        self.__ocsp_list = dbcontent.certificate_ocsp_list()
        
        ocsp_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ocsp_list))
        ca_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ca_list))
        ca_Key = list(filter(lambda c: c["iskey"] == "1", self.__ca_list))

        issuer_key = asymmetric.load_private_key(os.path.join(self.__base_path, ca_Key[0]["filename"]))
        issuer_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ca_NoKey[0]["filename"]))
        subject_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ocsp_NoKey[0]["filename"]))

        #inicializamos una fecha de revoke, dummy
        revoked_time = datetime(2015, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
        builder = OCSPResponseBuilder('successful', subject_cert, 'key_compromise', revoked_time)
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']
        
        #print(response_data)
        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)

        #self.assertEqual('revoked', cert_response['cert_status'].name)
        #self.assertEqual(revoked_time, cert_response['cert_status'].chosen['revocation_time'].native)
        
        return der_bytes

    def test_build_revoked_no_reason(self):

        self.__base_path = glv.get_variable("FILES_REPO_DIR")
        if (self.__base_path == "Not Found"):
            sys.exit('global variable {}, is empty: {}'.format("FILES_REPO_DIR", self.__base_path))       

        self.__ca_list = dbcontent.certificate_ca_list()
        self.__ocsp_list = dbcontent.certificate_ocsp_list()
        
        ocsp_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ocsp_list))
        ca_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ca_list))
        ca_Key = list(filter(lambda c: c["iskey"] == "1", self.__ca_list))

        issuer_key = asymmetric.load_private_key(os.path.join(self.__base_path, ca_Key[0]["filename"]))
        issuer_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ca_NoKey[0]["filename"]))
        subject_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ocsp_NoKey[0]["filename"]))

        #inicializamos una fecha de revoke, dummy
        revoked_time = datetime(2015, 9, 1, 12, 0, 0, tzinfo=timezone.utc)
        builder = OCSPResponseBuilder('successful', subject_cert, 'revoked', revoked_time)
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        #print(response_data)

        cert_response = response_data['responses'][0]

        #self.assertEqual('revoked', cert_response['cert_status'].name)
        #self.assertEqual(revoked_time, cert_response['cert_status'].chosen['revocation_time'].native)
        #self.assertEqual('unspecified', cert_response['cert_status'].chosen['revocation_reason'].native)

        return der_bytes
    
    def test_build_delegated_good_response(self):

        self.__base_path = glv.get_variable("FILES_REPO_DIR")
        if (self.__base_path == "Not Found"):
            sys.exit('global variable {}, is empty: {}'.format("FILES_REPO_DIR", self.__base_path))       

        self.__ca_list = dbcontent.certificate_ca_list()
        self.__ocsp_list = dbcontent.certificate_ocsp_list()
        
        ca_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ca_list))
        ocsp_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ocsp_list))
        ocsp_Key = list(filter(lambda c: c["iskey"] == "1", self.__ocsp_list))
        
        responder_key = asymmetric.load_private_key(os.path.join(self.__base_path, ocsp_Key[0]["filename"]))
        responder_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ocsp_NoKey[0]["filename"]))
        issuer_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ca_NoKey[0]["filename"]))
        subject_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ocsp_NoKey[0]["filename"]))

        builder = OCSPResponseBuilder('successful', subject_cert, 'good')
        builder.certificate_issuer = issuer_cert
        ocsp_response = builder.build(responder_key, responder_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        #print(response_data)
        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        
        cert_response = response_data['responses'][0]

        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)

        #self.assertEqual('good', cert_response['cert_status'].name)
        #self.assertGreaterEqual(datetime.now(timezone.utc), cert_response['this_update'].native)
        return der_bytes
        
    def test_build_unknown_response(self):

        self.__base_path = glv.get_variable("FILES_REPO_DIR")
        if (self.__base_path == "Not Found"):
            sys.exit('global variable {}, is empty: {}'.format("FILES_REPO_DIR", self.__base_path))       

        self.__ca_list = dbcontent.certificate_ca_list()
        self.__ocsp_list = dbcontent.certificate_ocsp_list()
        
        ocsp_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ocsp_list))
        ca_NoKey = list(filter(lambda c: c["iskey"] == "0", self.__ca_list))
        ca_Key = list(filter(lambda c: c["iskey"] == "1", self.__ca_list))
        
        issuer_key = asymmetric.load_private_key(os.path.join(self.__base_path, ca_Key[0]["filename"]))
        issuer_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ca_NoKey[0]["filename"]))
        subject_cert = asymmetric.load_certificate(os.path.join(self.__base_path, ocsp_NoKey[0]["filename"]))

        builder = OCSPResponseBuilder('successful', subject_cert, 'unknown')
        ocsp_response = builder.build(issuer_key, issuer_cert)
        der_bytes = ocsp_response.dump()

        new_response = asn1crypto.ocsp.OCSPResponse.load(der_bytes)
        basic_response = new_response['response_bytes']['response'].parsed
        response_data = basic_response['tbs_response_data']

        #print(response_data)
        #self.assertGreaterEqual(datetime.now(timezone.utc), response_data['produced_at'].native)
        
        cert_response = response_data['responses'][0]

        #self.assertEqual(subject_cert.asn1.serial_number, cert_response['cert_id']['serial_number'].native)

        #self.assertEqual('unknown', cert_response['cert_status'].name)
        #self.assertGreaterEqual(datetime.now(timezone.utc), cert_response['this_update'].native)
        
        return der_bytes
    
    def test_build_error_response(self):
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
