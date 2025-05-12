# -*- coding: UTF-8 -*-

from http.server import BaseHTTPRequestHandler, HTTPServer
import base64
import re
import time
import json
from datetime import datetime
import os

#!pip install aiohttp
import aiohttp

from pyasn1.codec.der import decoder
from pyasn1_modules import rfc2560, rfc5280, rfc6960
from pyasn1_modules import pem

from cryptography.hazmat.primitives import serialization

import lib.global_variable as glv
import lib.constants as cts
import lib.ocsp_response_helper as ocspHelper
import lib.dbcontent as dbcontent
from lib.managers import CertificateDummy as certManager

# Load global variable management module
glv.init_global_variable()
glv.set_variable("APP_NAME", "Web Api Application")
glv.set_variable("APP_PATH", os.path.dirname(__file__))
glv.set_variable("DATA_DIR", os.path.join(glv.get_variable("APP_PATH"), "data"))
glv.set_variable("DB_REPO_DIR",  os.path.join(glv.get_variable("DATA_DIR"), "dbRepository"))
glv.set_variable("FILES_REPO_DIR",  os.path.join(glv.get_variable("DATA_DIR"), "fileRepository"))


def parse_request_der(raw) -> str:
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
        #print(f"algorithm request: {ha['algorithm']}")
        #print(f"parameters request: {ha['parameters']}")
        #print(f"serialNumber: {req['reqCert']['serialNumber']}")
        return hex(req['reqCert']['serialNumber'])

class MyServerRequestHandler(BaseHTTPRequestHandler):

  def do_POST(self):
    if 'content-type' in self.headers:
        app_type = self.headers['content-type']
    else:
        app_type = None

    #Para la validacion del ocsp, evaluamos el content-type a tratar.
    if app_type is not None and app_type == cts.OCSP_REQ_TYPE:

        print(f"invocando endpoint POST OCSP {cts.ENDPOINT_POST_OCSP}")

        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
        #imprime detalle
        serialNumber = parse_request_der(data)
        certificateFound = dbcontent.certificate_status_by_serialnumber(serialNumber)
        status = "revoke" #por defecto, revocamos el certificado.
        if (certificateFound is not None):
          status = certificateFound[0]['status']
        
        print(f'certificado con serial number {serialNumber} tiene un estado {status}')
              
        self.send_response(200)
        self.send_header('Content-type', cts.OCSP_REP_TYPE)
        self.end_headers()
        if (status=="active"):
          print(f'respuesta ocsp al certificado con serial number {serialNumber} es GOOD')
          #self.wfile.write(ocspHelper.OCSPResponseBuilderTests.test_build_good_response())
          self.wfile.write(ocspHelper.OCSPResponseBuilderTests.test_build_delegated_good_response(self))
        else:
          print(f'respuesta ocsp al certificado con serial number {serialNumber} es REVOKE')
          self.wfile.write(ocspHelper.OCSPResponseBuilderTests.test_build_revoked_response(self))

    elif None != re.search(cts.ENDPOINT_POST_SIGN_DOCUMENT, self.path):

      print(f"invocando endpoint POST {cts.ENDPOINT_POST_SIGN_DOCUMENT}")

      if app_type is not None and app_type == cts.JSON_REQ_TYPE:
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
      else:
        data = b'{"cuit":"", "pdfBase64":""}'

      ascii_msg = data.decode('ascii')
      # Json library convert stirng dictionary to real dictionary type.
      # Double quotes is standard format for json
      ascii_msg = ascii_msg.replace("'", "\"")
      output_dict = json.loads(ascii_msg) # convert string dictionary to dict format

      if (output_dict['cuit'] is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return
               
      if (output_dict['pdfBase64'] is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del archivo en base64')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      certificateFound = dbcontent.pkcs12_active_by_username(output_dict['cuit'])
      if (certificateFound is not None):
        fileNameToCreate = "%s-%s-%d" %("pdf",output_dict['cuit'], time.time())
        pdfPathPending = certManager.saveDocumentOnDisk(self, 
                                                        glv.get_variable("FILES_REPO_DIR"), 
                                                        fileNameToCreate, 
                                                        output_dict['pdfBase64'])
        dbUpdated = dbcontent.save_documents_by_username(output_dict['cuit'], pdfPathPending)
        base64_encoded = None
        if (dbUpdated is False):
          self.send_response(400, 'Bad Request: No es posible guardar el documento en nuestro repositorio')
          self.send_header('Content-Type', 'application/json')
          self.end_headers()
        else:   
          documentsList = dbcontent.documents_list_by_username_filename(output_dict['cuit'], pdfPathPending)
          pdfPathPendingID = documentsList[0]["id"]
          
          fileNameToCreate = "%s-%s-%d-signed.pdf" %("pdf",output_dict['cuit'], time.time())
          pdfOuputPathFile = certManager.signPdfWithPKCS12(
                                      glv.get_variable("FILES_REPO_DIR"),
                                      certificateFound[0]["filename"], 
                                      output_dict['cuit'], 
                                      pdfPathPending, 
                                      fileNameToCreate)
          if (pdfOuputPathFile is not None):
            dbUpdated = dbcontent.update_complete_document_by_username(
                              output_dict['cuit'], 
                              pdfPathPendingID, 
                              pdfOuputPathFile)
            if (dbUpdated is False):
              self.send_response(400, 'Bad Request: No es posible actualizar el documento en nuestro repositorio')
              self.send_header('Content-Type', 'application/json')
              self.end_headers()
            else:
              base64_encoded = certManager.getDocumentAsBase64(pdfOuputPathFile)
              if (base64_encoded is not None):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', int(len(base64_encoded)))
                self.end_headers()
                try:
                  self.wfile.write(base64_encoded.encode('utf-8'))
                except Exception as e:
                  print(f"An error occurred: {e}")
              else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', int(len(base64_encoded)))
                self.end_headers()
              return
          else:
            self.send_response(400, 'Bad Request: No es posible firmar documento')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
          return          
      else:
        self.send_response(400, 'Bad Request: cuit no posee un certificado activo')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    elif None != re.search(cts.ENDPOINT_POST_SIGN, self.path):

      print(f"invocando endpoint POST {cts.ENDPOINT_POST_SIGN}")

      if app_type is not None and app_type == cts.JSON_REQ_TYPE:
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
      else:
        data = b'{"cuit":"","fileID":""}'

      ascii_msg = data.decode('ascii')
      # Json library convert stirng dictionary to real dictionary type.
      # Double quotes is standard format for json
      ascii_msg = ascii_msg.replace("'", "\"")
      output_dict = json.loads(ascii_msg) # convert string dictionary to dict format

      if (output_dict['cuit'] is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return
               
      if (output_dict['fileID'] is None):
        self.send_response(400, 'Bad Request: Se requiere Id de archivo seleccionado')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      certificateFound = dbcontent.pkcs12_active_by_username(output_dict['cuit'])
      if (certificateFound is not None):
        documentsList = dbcontent.documents_list_by_username_fileId(output_dict['cuit'], output_dict['fileID'])
        pdfPathPending = documentsList[0]["filename"]
        pdfPathPendingID = output_dict['fileID']
        if (documentsList is None):
          self.send_response(400, 'Bad Request: No se encuentran documentos para la condicion solicitada')
          self.send_header('Content-Type', 'application/json')
          self.end_headers()
        else:   
          fileNameToCreate = "%s-%s-%d-signed.pdf" %("pdf",output_dict['cuit'], time.time())
          pdfOuputPathFile = certManager.signPdfWithPKCS12(
                                      glv.get_variable("FILES_REPO_DIR"),
                                      certificateFound[0]["filename"], 
                                      output_dict['cuit'], 
                                      pdfPathPending, 
                                      fileNameToCreate)
                       
          if (pdfOuputPathFile is not None):
            dbUpdated = dbcontent.update_complete_document_by_username(
                              output_dict['cuit'], 
                              pdfPathPendingID, 
                              pdfOuputPathFile)
            if (dbUpdated is False):
              self.send_response(400, 'Bad Request: No es posible actualizar el documento en nuestro repositorio')
              self.send_header('Content-Type', 'application/json')
              self.end_headers()
            else:
              base64_encoded = certManager.getDocumentAsBase64(pdfOuputPathFile)
              if (base64_encoded is not None):
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', int(len(base64_encoded)))
                self.end_headers()
                try:
                  self.wfile.write(base64_encoded.encode('utf-8'))
                except Exception as e:
                  print(f"An error occurred: {e}")
              else:
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.send_header('Content-Length', int(len(base64_encoded)))
                self.end_headers()
              return
        self.send_response(400, 'Bad Request: No es posible firmar documento')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

      else:
        self.send_response(400, 'Bad Request: cuit no posee un certificado activo')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    elif None != re.search(cts.ENDPOINT_POST_UPLOAD_DOCUMENT, self.path):

      print(f"invocando endpoint POST {cts.ENDPOINT_POST_UPLOAD_DOCUMENT}")

      if app_type is not None and app_type == cts.JSON_REQ_TYPE:
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
      else:
        data = b'{"cuit":"","filename":"","pdfBase64":""}'

      ascii_msg = data.decode('ascii')
      # Json library convert stirng dictionary to real dictionary type.
      # Double quotes is standard format for json
      ascii_msg = ascii_msg.replace("'", "\"")
      output_dict = json.loads(ascii_msg) # convert string dictionary to dict format

      if (output_dict['cuit'] is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return
      
      if (output_dict['pdfBase64'] is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del archivo en base64')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      certificateFound = dbcontent.pkcs12_active_by_username(output_dict['cuit'])
      if (certificateFound is not None):
        fileNameToCreate = "%s-%s-%d" %("pdf",output_dict['cuit'], time.time())
        #if (output_dict['filename'] is not None):
        #  fileNameToCreate = "%s-%s-%d" %("pdf", output_dict['filename'], time.time())
        
        pdfPathPending = certManager.saveDocumentOnDisk(self, 
                                                        glv.get_variable("FILES_REPO_DIR"), 
                                                        fileNameToCreate, 
                                                        output_dict['pdfBase64'])
        dbUpdated = dbcontent.save_documents_by_username(
                              output_dict['cuit'], 
                              pdfPathPending)
        base64_encoded = None
        if (dbUpdated is False):
          self.send_response(400, 'Bad Request: No es posible guardar el documento en nuestro repositorio')
          self.send_header('Content-Type', 'application/json')
          self.end_headers()
        else:   
          if (pdfPathPending is not None):
            base64_encoded = certManager.getDocumentAsBase64(pdfPathPending)
            if (base64_encoded is not None):
              self.send_response(200)
              self.send_header('Content-Type', 'application/json')
              self.send_header('Content-Length', int(len(base64_encoded)))
              self.end_headers()
              try:
                self.wfile.write(base64_encoded.encode('utf-8'))
              except Exception as e:
                print(f"An error occurred: {e}")
            else:
              self.send_response(200)
              self.send_header('Content-Type', 'application/json')
              self.send_header('Content-Length', int(len(base64_encoded)))
              self.end_headers()
            return
          else:
            self.send_response(400, 'Bad Request: No es posible preservar el documento')
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
      else:
        self.send_response(400, 'Bad Request: cuit no posee un certificado activo')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    elif None != re.search(cts.ENDPOINT_POST_LOGIN, self.path):

      print(f"invocando endpoint POST {cts.ENDPOINT_POST_LOGIN}")

      if app_type is not None and app_type == cts.JSON_REQ_TYPE:
        length = int(self.headers['content-length'])
        data = self.rfile.read(length)
      else:
        data = b'{"username":"","password":""}'

      ascii_msg = data.decode('ascii')
      # Json library convert stirng dictionary to real dictionary type.
      # Double quotes is standard format for json
      ascii_msg = ascii_msg.replace("'", "\"")
      output_dict = json.loads(ascii_msg) # convert string dictionary to dict format
      #print(output_dict)
      userFound = dbcontent.user_login(output_dict['username'],output_dict['password'])
      if (userFound == True):
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
      else:
        self.send_response(400, 'Bad Request: usuario no existe o informacion no valida')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    return



  def do_GET(self):

    #match_object_match = re.search(cts.ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID, self.path)
    #match_object_search = re.match(f'(.*?){cts.ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID}', self.path)
    #print(match_object_search )
    #if (match_object_search is not None):
    #  print(match_object_search.group() )

    #print(match_object_match )
    #if (match_object_match is not None):
    #  print(match_object_match.group() )

    if None != re.search(cts.ENDPOINT_GET_HEALTH, self.path):

      print(f"invocando endpoint GET {cts.ENDPOINT_GET_HEALTH}")
      
      self.send_response(200)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
      self.wfile.write("OK".encode('utf-8'))

    elif None != re.search(cts.ENDPOINT_GET_TIMESTAMP, self.path):
        
      print(f"invocando endpoint GET {cts.ENDPOINT_GET_TIMESTAMP}")
      
      self.send_response(200)
      self.send_header('Content-type', 'application/json')
      self.end_headers()
      timestamp = int(time.time())
      datetime_obj = datetime.fromtimestamp(timestamp)
      formatted_datetime = datetime_obj.isoformat()
      response_data = {'timestamp': timestamp, 'datetime': formatted_datetime}
      self.wfile.write(json.dumps(response_data).encode('utf-8'))

    elif None != re.search(cts.ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID, self.path):
      
      cuit = self.path.split('/')[-2]
      fileID = self.path.split('/')[-1]

      if (cuit is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      if (fileID is None):
        self.send_response(400, 'Bad Request: Se requiere ID de archivo seleccionado')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      print(f"invocando endpoint GET {cts.ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID} con cuit {cuit} y FileId {fileID}")

      documentsFound = dbcontent.documents_list_by_username_fileId(cuit, fileID)

      if documentsFound is not None:
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

        if (documentsFound[0]["fileSigned"] is not None):
          base64_encoded = certManager.getDocumentAsBase64(documentsFound[0]["fileSigned"])
          documentsFound[0]["base64File"] = base64_encoded
        else:
          base64_encoded = certManager.getDocumentAsBase64(documentsFound[0]["filename"])
          documentsFound[0]["base64File"] = base64_encoded

        jsonResp = json.dumps(documentsFound)
        self.send_header('Content-Length', int(len(jsonResp)))
        self.wfile.write(jsonResp.encode('utf-8'))
        
      else:

        self.send_response(400, 'Bad Request: cuit or fileId, does not exist')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
      
  
    elif None != re.search(cts.ENDPOINT_GET_CERTIFICATE_BY_CUIT_CERTID, self.path):
      
      cuit = self.path.split('/')[-2]
      certID = self.path.split('/')[-1]

      if (cuit is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      if (certID is None):
        self.send_response(400, 'Bad Request: Se requiere ID de certificado seleccionado')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      print(f"invocando endpoint GET {cts.ENDPOINT_GET_CERTIFICATE_BY_CUIT_CERTID} con cuit {cuit} y CertId {certID}")

      certsFound = dbcontent.certificate_list_by_username_certId(cuit, certID)

      if (certsFound is not None):
        
        certPathFile = os.path.join(glv.get_variable("FILES_REPO_DIR"), certsFound[0]["filename"])
        cert_data = certManager.getCertificateAuthority(certPathFile, None)        
        bytes_response = cert_data.cert.pem
        self.send_response(200)
        self.send_header('Content-type', 'application/pkix-cert')
        self.send_header('Accept-Ranges','bytes')
        # application/x-pem-file: This is commonly used for certificates, certificate requests (CSRs), and CRLs in PEM format (Base64 encoded).
        # application/pkix-cert: This can be used for single certificates in DER format.
        # application/pkix-crl: This is for CRLs (Certificate Revocation Lists) in DER format.
        # application/pkcs10: This is used for PKCS#10 certificate signing requests.
        # application/x-pkcs7-mime: This is used for PKCS#7 messages, which may contain certificates or CRLs, often in binary (DER) format.
        if (bytes_response is not None):
          self.send_header('Content-Length', int(len(bytes_response)))

        self.end_headers()
        
        if (bytes_response is not None):
          try:
            self.wfile.write(bytes_response)
          except Exception as e:
              print(f"An error occurred: {e}")
        
        return
      
      else:

        self.send_response(400, 'Bad Request: cuit or certId, does not exist')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()

    elif None != re.search(cts.ENDPOINT_GET_DOCUMENTS_BY_CUIT, self.path):

      cuit = self.path.split('/')[-1]

      if (cuit is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return
               
      print(f"invocando endpoint GET {cts.ENDPOINT_GET_DOCUMENTS_BY_CUIT} con cuit {cuit}")
      
      documentsFound = dbcontent.documents_list_by_username(cuit)
      if documentsFound is not None:
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(documentsFound).encode('utf-8'))
      else:
        self.send_response(400, 'Bad Request: cuit does not exist')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()


    elif None != re.search(cts.ENDPOINT_GET_CRT, self.path):

        print(f"invocando endpoint GET {cts.ENDPOINT_GET_CRT}")

        certificatesCAFound = dbcontent.certificate_ca_list()
        ca_NoKey = list(filter(lambda c: c["iskey"] == "0", certificatesCAFound))
        ca_Key = list(filter(lambda c: c["iskey"] == "1", certificatesCAFound))
        caNoKeyPathFile = os.path.join(glv.get_variable("FILES_REPO_DIR"), ca_NoKey[0]["filename"])
        caKeyPathFile = os.path.join(glv.get_variable("FILES_REPO_DIR"), ca_Key[0]["filename"])
        
        cert_data = certManager.getCertificateAuthority(caNoKeyPathFile, caKeyPathFile)        
        #bytes_response = base64.b64encode(cert_data.cert.pem).decode("ascii")
        bytes_response = cert_data.cert.pem
        self.send_response(200)
        self.send_header('Content-type', 'application/x-x509-ca-cert')
        self.send_header('Accept-Ranges','bytes')
        # application/x-pem-file: This is commonly used for certificates, certificate requests (CSRs), and CRLs in PEM format (Base64 encoded).
        # application/pkix-cert: This can be used for single certificates in DER format.
        # application/pkix-crl: This is for CRLs (Certificate Revocation Lists) in DER format.
        # application/pkcs10: This is used for PKCS#10 certificate signing requests.
        # application/x-pkcs7-mime: This is used for PKCS#7 messages, which may contain certificates or CRLs, often in binary (DER) format.
        if (bytes_response is not None):
          self.send_header('Content-Length', int(len(bytes_response)))

        self.end_headers()
        if (bytes_response is not None):
          try:
            #self.wfile.write(bytes_response.encode('utf-8'))
            self.wfile.write(bytes_response)
          except Exception as e:
              print(f"An error occurred: {e}")
        
    elif None != re.search(cts.ENDPOINT_GET_CRL, self.path):
              
        print(f"invocando endpoint GET {cts.ENDPOINT_GET_CRL}")

        certificatesCRLFound = dbcontent.certificate_crl_list()
        crl_NoKey = list(filter(lambda c: c["iskey"] == "0", certificatesCRLFound))
        crlNoKeyPathFile = os.path.join(glv.get_variable("FILES_REPO_DIR"), crl_NoKey[0]["filename"])
        
        cert_data = certManager.getCRLCertificate(crlNoKeyPathFile)        
        bytes_response = cert_data.cert.pem

        self.send_response(200)
        self.send_header('Content-type', 'application/pkix-crl')
        self.send_header('Accept-Ranges','bytes')
        self.end_headers()
        # application/pkix-crl: This is for CRLs (Certificate Revocation Lists) in DER format.
        if (bytes_response is not None):
          self.send_header('Content-Length', int(len(bytes_response)))

        self.end_headers()
        if (bytes_response is not None):
          try:
            #self.wfile.write(bytes_response.encode('utf-8'))
            self.wfile.write(bytes_response)
          except Exception as e:
              print(f"An error occurred: {e}")

    elif None != re.search(cts.ENDPOINT_GET_CERTIFICATE_BY_CUIT, self.path):
      
      cuit = self.path.split('/')[-1]

      if (cuit is None):
        self.send_response(400, 'Bad Request: Se requiere informacion del cuit')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        return

      print(f"invocando endpoint GET {cts.ENDPOINT_GET_CERTIFICATE_BY_CUIT} con cuit {cuit}")

      certificatesFound = dbcontent.certificate_list_by_username(cuit)
      if certificatesFound is not None:
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(certificatesFound).encode('utf-8'))
      else:
        self.send_response(400, 'Bad Request: cuit does not exist')
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
    else:
      self.send_response(403)
      self.send_header('Content-Type', 'application/json')
      self.end_headers()
    
    return



  def do_PUT(self):
      print("Received PUT")
      content_length_str = self.headers.get('Content-Length')
      if content_length_str is None:
          content_length_str = '0'

      content_length = int(content_length_str)
      data = self.rfile.read(content_length)
      print("Received PUT data:", data.decode('utf-8'))

      # Send a success response
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'PUT request received successfully')



  def do_PATCH(self):
      print("Received PATCH")
      content_length_str = self.headers.get('Content-Length')
      if content_length_str is None:
          content_length_str = '0'

      content_length = int(content_length_str)
      data = self.rfile.read(content_length)
      print("Received PATCH data:", data.decode('utf-8'))

      # Send a success response
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'PATCH request received successfully')




  def do_DELETE(self):
      print("Received DELETE")
      content_length_str = self.headers.get('Content-Length')
      if content_length_str is None:
          content_length_str = '0'

      content_length = int(content_length_str)
      data = self.rfile.read(content_length)
      print("Received DELETE data:", data.decode('utf-8'))

      # Send a success response
      self.send_response(200)
      self.send_header('Content-type', 'text/plain')
      self.end_headers()
      self.wfile.write(b'DELETE request received successfully')


def main():
    # Set the server address and port
    server_address = ('', cts.PORT)
    # Create an instance of the HTTP server
    with HTTPServer(server_address, MyServerRequestHandler) as httpd:
        print('Starting server...')
        print(f"Serving at port {cts.PORT}")
        httpd.serve_forever()
    
if __name__ == '__main__':
    main()
