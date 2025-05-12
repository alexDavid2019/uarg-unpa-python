# -*- coding:utf-8-*-

import os
import requests
import lib.global_variable as glv
import lib.constants as cts
import json

class RequestHelper(object):

    """request helper"""

    def check_server_status(self, url):
        try:
            #ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            #headers = {'User-Agent': ua, 'Content-type': 'application/json', 'Accept': 'text/plain'}
            #response = requests.get(url, headers)
            response = requests.get(url)
            if response.status_code == 200:
                return True, response.text
            else:
                return False, f"Status code: {response.status_code}"
        except requests.exceptions.RequestException as e:
            return False, f"Error: {e}"
            
    def __init__(self):
        self.image_path = os.path.join(glv.get_variable("APP_PATH"), glv.get_variable("DATA_DIR"), 'image')
        glv.set_variable("SERVER_ACTIVE",None)

    #Metodo privado
    def __check_isServerActive(self):
        message=""
        if (glv.get_variable("SERVER_ACTIVE") is None):
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_GET_HEALTH)
            is_running, message = self.check_server_status(self, api_url)
            glv.set_variable("SERVER_ACTIVE",is_running)
        
        if (glv.get_variable("SERVER_ACTIVE") is False or glv.get_variable("SERVER_ACTIVE") is None):
            print(f"Server is not running or API is down. {message}")
            raise Exception("Server is not running or API is down")

    def user_login(self, username, password):
        try:

            self.__check_isServerActive(self)

            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_POST_LOGIN)

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/json'}
            _dataArg = {
                "username": username,
                "password": password
            }

            response = requests.post(api_url, json=_dataArg,headers=_headers)

            if response.status_code == 200:
                return True, response.text
            else:
                return False, f"Status code: {response.status_code} {response.text}"
        except requests.exceptions.RequestException as e:
            return False, f"Error: {e}"

    def documents_by_user(self, username):
        try:
            
            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_GET_DOCUMENTS_BY_CUIT.replace("[cuit]",username))

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/json'}

            response = requests.get(api_url, headers=_headers)
        
            if response.status_code == 200:
                binary = response.content
                json_obj = json.loads(binary)
                return json_obj               
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def certificates_by_user(self, username):
        try:

            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_GET_CERTIFICATE_BY_CUIT.replace("[cuit]",username))

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/json'}

            response = requests.get(api_url, headers=_headers)
        
            if response.status_code == 200:
                binary = response.content
                json_obj = json.loads(binary)
                return json_obj               
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
    
    def certificate_by_user_certId(self, username, id):
        try:

            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_GET_CERTIFICATE_BY_CUIT_CERTID.replace("[cuit]",username).replace("[id]",id))

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/pkix-cert'}

            response = requests.get(api_url, headers=_headers)

            if response.status_code == 200:
                binary = response.content
                return binary               
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    def document_by_user_certId(self, username, id):
        try:

            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_GET_DOCUMENT_BY_CUIT_FILEID.replace("[cuit]",username).replace("[id]",id))

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/pkix-cert'}

            response = requests.get(api_url, headers=_headers)

            if response.status_code == 200:
                binary = response.content
                json_obj = json.loads(binary)
                return json_obj
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return None
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return None
        
    def document_add_by_user(self, username, base64Data) -> bool:
        try:

            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_POST_UPLOAD_DOCUMENT)

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/json'}
            _dataArg = {
                "cuit": username,
                "pdfBase64": base64Data
            }
            response = requests.post(api_url, json=_dataArg,headers=_headers)
            if response.status_code == 200:
                binary = response.content
                return (binary is not None)
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return False


    def document_add_sign_by_user(self, username, base64Data) -> bool:
        try:

            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_POST_SIGN_DOCUMENT)

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/json'}
            _dataArg = {
                "cuit": username,
                "pdfBase64": base64Data
            }
            response = requests.post(api_url, json=_dataArg,headers=_headers)
            if response.status_code == 200:
                binary = response.content
                return (binary is not None)
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return False


    def document_sign_by_id(self, username, fileID) -> bool:
        try:

            self.__check_isServerActive(self)
            
            api_url = "%s%s" % (cts.HOST_API, cts.ENDPOINT_POST_SIGN)

            ua = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'
            _headers = {'User-Agent': ua, 'Content-type': 'application/json'}
            _dataArg = {
                "cuit": username,
                "fileID": fileID
            }
            response = requests.post(api_url, json=_dataArg,headers=_headers)
            if response.status_code == 200:
                binary = response.content
                return (binary is not None)
            else:
                print(f"Status code: {response.status_code} {response.text}")
                return False
        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            return False
