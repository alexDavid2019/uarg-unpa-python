#!pip install pyasn1
#!pip install pyasn1-modules

import sys, os, base64, logging

from http.server import BaseHTTPRequestHandler, HTTPServer

from pyasn1.codec.der import decoder
from pyasn1_modules import rfc2560, rfc5280, rfc6960
from pyasn1_modules import pem

from ocsp_response_builder import OCSPResponseBuilderTests as ocspRespTest

import time
import json
from datetime import datetime

OCSP_REQ_TYPE = 'application/ocsp-request'
OCSP_REP_TYPE = 'application/ocsp-response'

certsRepo = "certsRepo"

path_root = os.path.dirname(__file__)
certsRepo_dir = os.path.join(path_root, 'certsRepo')

FORMAT = "%(asctime)s %(levelname)s in process %(process)d - %(message)s"
logging.basicConfig(filename=os.path.join(certsRepo_dir, 'ocsp_py.log'), encoding='utf-8', level=logging.INFO, format=FORMAT)

ocsp_resp_dummy_pem_text = """\
MIIEvQoBAKCCBLYwggSyBgkrBgEFBQcwAQEEggSjMIIEnzCCAQ+hgYAwfjELMAkGA1UEBhMCQVUx
EzARBgNVBAgTClNvbWUtU3RhdGUxITAfBgNVBAoTGEludGVybmV0IFdpZGdpdHMgUHR5IEx0ZDEV
MBMGA1UEAxMMc25tcGxhYnMuY29tMSAwHgYJKoZIhvcNAQkBFhFpbmZvQHNubXBsYWJzLmNvbRgP
MjAxMjA0MTExNDA5MjJaMFQwUjA9MAkGBSsOAwIaBQAEFLdmsxX0LkOSjTdofXdwRl6mmDfCBBSS
pHUspJ6+gUTrefyKxZWl6xB1cwIENd70z4IAGA8yMDEyMDQxMTE0MDkyMlqhIzAhMB8GCSsGAQUF
BzABAgQSBBBjdJOiIW9EKJGELNNf/rdAMA0GCSqGSIb3DQEBBQUAA4GBADk7oRiCy4ew1u0N52QL
RFpW+tdb0NfkV2Xyu+HChKiTThZPr9ZXalIgkJ1w3BAnzhbB0JX/zq7Pf8yEz/OrQ4GGH7HyD3Vg
PkMu+J6I3A2An+bUQo99AmCbZ5/tSHtDYQMQt3iNbv1fk0yvDmh7UdKuXUNSyJdHeg27dMNy4k8A
oIIC9TCCAvEwggLtMIICVqADAgECAgEBMA0GCSqGSIb3DQEBBQUAMH4xCzAJBgNVBAYTAkFVMRMw
EQYDVQQIEwpTb21lLVN0YXRlMSEwHwYDVQQKExhJbnRlcm5ldCBXaWRnaXRzIFB0eSBMdGQxFTAT
BgNVBAMTDHNubXBsYWJzLmNvbTEgMB4GCSqGSIb3DQEJARYRaW5mb0Bzbm1wbGFicy5jb20wHhcN
MTIwNDExMTMyNTM1WhcNMTMwNDExMTMyNTM1WjB+MQswCQYDVQQGEwJBVTETMBEGA1UECBMKU29t
ZS1TdGF0ZTEhMB8GA1UEChMYSW50ZXJuZXQgV2lkZ2l0cyBQdHkgTHRkMRUwEwYDVQQDEwxzbm1w
bGFicy5jb20xIDAeBgkqhkiG9w0BCQEWEWluZm9Ac25tcGxhYnMuY29tMIGfMA0GCSqGSIb3DQEB
AQUAA4GNADCBiQKBgQDDDU5HOnNV8I2CojxB8ilIWRHYQuaAjnjrETMOprouDHFXnwWqQo/I3m0b
XYmocrh9kDefb+cgc7+eJKvAvBqrqXRnU38DmQU/zhypCftGGfP8xjuBZ1n23lR3hplN1yYA0J2X
SgBaAg6e8OsKf1vcX8Es09rDo8mQpt4G2zR56wIDAQABo3sweTAJBgNVHRMEAjAAMCwGCWCGSAGG
+EIBDQQfFh1PcGVuU1NMIEdlbmVyYXRlZCBDZXJ0aWZpY2F0ZTAdBgNVHQ4EFgQU8Ys2dpJFLMHl
yY57D4BNmlqnEcYwHwYDVR0jBBgwFoAU8Ys2dpJFLMHlyY57D4BNmlqnEcYwDQYJKoZIhvcNAQEF
BQADgYEAWR0uFJVlQId6hVpUbgXFTpywtNitNXFiYYkRRv77McSJqLCa/c1wnuLmqcFcuRUK0oN6
8ZJDP2HDDKe8MCZ8+sx+CF54eM8VCgN9uQ9XyE7x9XrXDd3Uw9RJVaWSIezkNKNeBE0lDM2jUjC4
HAESdf7nebz1wtqAOXE1jWF/y8g=
"""

def parse_request_der(raw):
    #https://github.com/etingof/pyasn1-modules/blob/master/tests/test_rfc6960.py
    #return tupple
    asn1Object, rest = decoder.decode(raw, asn1Spec=rfc2560.OCSPRequest())
    #print(asn1Object.prettyPrint())
    print(f"Version Request:{asn1Object['tbsRequest']['version']}")
    for extn in asn1Object['tbsRequest']['requestExtensions']:
        ev, rest = decoder.decode(extn['extnValue'],asn1Spec=rfc5280.certificateExtensionsMap[extn['extnID']])
        print(ev.prettyPrint())
    for req in  asn1Object['tbsRequest']['requestList']:
        ha = req['reqCert']['hashAlgorithm']
        print(f"algorithm request: {ha['algorithm']}")
        print(f"parameters request: {ha['parameters']}")
        print(f"serialNumber: {req['reqCert']['serialNumber']}")
        print(f"serialNumber HEX: {hex(req['reqCert']['serialNumber'])}")

def parse_response_dummy_pem():
    #https://github.com/etingof/pyasn1-modules/blob/master/tests/test_rfc6960.py
    substrate = pem.readBase64fromText(ocsp_resp_dummy_pem_text)
    asn1Object, rest = decoder.decode(substrate, asn1Spec=rfc6960.OCSPResponse())
    print(asn1Object.prettyPrint())
    print(f"responseStatus: {asn1Object['responseStatus']}")
    rb = asn1Object['responseBytes']
    resp, rest = decoder.decode(rb['response'], asn1Spec=rfc6960.ocspResponseMap[rb['responseType']])
    print(resp.prettyPrint())
    for extn in resp['tbsResponseData']['responseExtensions']:
        ev, rest = decoder.decode(extn['extnValue'],asn1Spec=rfc5280.certificateExtensionsMap[extn['extnID']])
        print(ev.prettyPrint())


# Define the HTTP request handler class
class MyRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        print("Received GET")
        if self.path == '/timestamp':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            timestamp = int(time.time())
            datetime_obj = datetime.fromtimestamp(timestamp)
            formatted_datetime = datetime_obj.isoformat()
            response_data = {'timestamp': timestamp, 'datetime': formatted_datetime}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-type', 'text/plain')
            self.end_headers()
            self.wfile.write(b'Not found')


        #self.send_response(200)
        #self.send_header('Content-type', 'text/html')
        #self.end_headers()
        #self.wfile.write(html_content)
    
    def do_POST(self, *args, **kwargs):
        print("Received POST")
        if 'content-type' in self.headers:
            app_type = self.headers['content-type']
        else:
            app_type = None

        if 'content-length' in self.headers and app_type == OCSP_REQ_TYPE:
            length = int(self.headers['content-length'])
            ocsp_request = self.rfile.read(length)
            #imprime detalle
            parse_request_der(ocsp_request)
            pass

        #Mostramos como parsear en ocsp response
        #parse_response_dummy_pem()

        self.send_response(200)
        self.send_header('Content-type', OCSP_REP_TYPE)
        self.end_headers()
        #self.wfile.write(ocspRespTest.test_build_good_response())
        #self.wfile.write(ocspRespTest.test_build_delegated_good_response())
        self.wfile.write(ocspRespTest.test_build_revoked_response())

    def do_PUT(self):
        print("Received PUT")
        content_length_str = self.headers.get('Content-Length')
        if content_length_str is None:
            content_length_str = '0'

        content_length = int(content_length_str)
        put_data = self.rfile.read(content_length)
        print("Received PUT data:", put_data.decode('utf-8'))

        # Send a success response
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(b'PUT request received successfully')

# Define the main function to start the server
def main():
    PORT = 8085
    # Set the server address and port
    server_address = ('', PORT)
    # Create an instance of the HTTP server
    with HTTPServer(server_address, MyRequestHandler) as httpd:
        print('Starting server...')
        print(f"Serving at port {PORT}")
        httpd.serve_forever()
    
if __name__ == '__main__':
    main()
