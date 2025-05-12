# -*- coding:utf-8-*-
import sys
import os
import time 

import lib.custom_serialization as serJson
import lib.global_variable as glv
from lib.custom_fileIO import *
from lib.managers import CertificateDummy as certManager

class CERHelper(object):
    """Certificate helper"""

    def __init__(self):
        #inicializamos variables
        self.base_path = glv.get_variable("FILES_REPO_DIR")

    def create_metadata(self):
        """create metadata from cvs file"""
        if (self.base_path == "Not Found"):
            sys.exit('global variable {}, is empty: {}'.format("FILES_REPO_DIR",self.base_path))       
        
        #creamos los dos certificados primarios y unicos
        fileNameToCreate = "%s-%d" %("ca_AutoSigned", time.time())
        #return tuple
        caCertPathFile,caKeyCertPathFile = certManager.generateCACertificate(self, pathRoot=self.base_path, 
                                                                             fileNameToWrite=fileNameToCreate,
                                                                             commonNameforOurCA="My First CA Certificate")

        fileNameToCreate = "%s-%d" %("ocsp_AutoSigned", time.time())
        #return tuple
        ocspPathFile, ocspKeyPathFile = certManager.generateOcspResponseCertificate(self,
                                                                                    pathRoot=self.base_path,
                                                                                    fileNameToWrite=fileNameToCreate,
                                                                                commonNameCert="OCSP Certificate To Response",
                                                                                pemFileCA=caCertPathFile,
                                                                                keyFileCA=caKeyCertPathFile)


        fileNameToCreate = "%s-%d" %("crl_revoked_certs", time.time())
        crlPathFile = certManager.generateCrlCertificate(self, pathRoot=self.base_path,
                                                                    fileNameToWrite=fileNameToCreate,
                                                                    pemFileCA=caCertPathFile,
                                                                    keyFileCA=caKeyCertPathFile)

        #tomamos un cvs como input de usuarios a registrar
        cvsPathFile = os.path.join(self.base_path, 'empresas_vigentes_tech.csv')
        #lo parseamos como diccionario porque tiene definido nombre de columna.  
        cvsDict = csv_to_dictionary(cvsPathFile)
        for registro in cvsDict:
            print(f"...procesing cuit: {registro["cuit"]}")
            
            fileNameToCreate = "%s-%s" %("csr_AutoSigned", registro["cuit"])
            #return tuple
            csrPathFile,csrKeyPathFile=certManager.generateCSRAutoSigned(self, pathRoot=self.base_path,
                                                                            fileNameToWrite=fileNameToCreate,
                                                                            pemFileCA=caCertPathFile,
                                                                            csr_common_name=f"cuit {registro["cuit"]}",
                                                                            csr_name_organization=registro["razonSocial"],
                                                                            csr_name_department=registro["localidad"],
                                                                            csr_email=registro["email"])
            fileNameToCreate = "%s-%s" %("cer_client", registro["cuit"])
            #return tuple
            cerPathFile, serialNumber = certManager.generateCertificate(self, pathRoot=self.base_path,
                                                                               fileNameToWrite=fileNameToCreate,
                                                                               commonNameCert=f"cuit {registro["cuit"]}",
                                                                               name_organization=registro["razonSocial"],
                                                                               name_department=registro["localidad"],
                                                                               email_Address=registro["email"], 
                                                                               pemFileCA=caCertPathFile, 
                                                                               keyFileCA=caKeyCertPathFile,
                                                                               csrFile=csrPathFile,
                                                                               csrKeyFile=csrKeyPathFile)
            
            fileNameToCreate = "%s-%s" %("p12_client", registro["cuit"])
            p12PathFile = certManager.generatePkcs12Certificate(self, pathRoot=self.base_path,
                                                                fileNameToWrite=fileNameToCreate,
                                                                commonNameCert=f"cuit {registro["cuit"]}",
                                                                passwordPkcs12=registro["cuit"],
                                                                cerPathFileGenerated=cerPathFile,
                                                                csrKeyFileGenerated=csrKeyPathFile)
            #Eliminamos los archivos no necesarios a partir de ahora.
            cleanFolderForFile(csrPathFile)
            cleanFolderForFile(csrKeyPathFile)
        
        print("...create metadata from files..")
        metadataDict = certManager.getMetadataFiles(self, path_dir=self.base_path) 
        #print(type(metadata)) #output <class 'dict'>
        print("...group metadata..")
        finalDict = {}
        for key, value in metadataDict.items(): #Returns key-value pairs
            if (key.startswith('ca_') and key.endswith('.crt')):
                if (finalDict.get("ca") is not None):
                    #list of dictionaries
                    finalDict["ca"] = [finalDict["ca"] , value]
                else:
                    finalDict["ca"] = value
            if (key.startswith('ca_') and key.endswith('.key')):
                if (finalDict.get("ca") is not None):
                    #list of dictionaries
                    finalDict["ca"] = [finalDict["ca"] , value]
                else:
                    finalDict["ca"] = value

            if (key.startswith('ocsp_') and key.endswith('.cer')):
                if (finalDict.get("ocsp") is not None):
                    #list of dictionaries
                    finalDict["ocsp"] = [finalDict["ocsp"] , value]
                else:
                    finalDict["ocsp"] = value
            if (key.startswith('ocsp_') and key.endswith('.key')):
                if (finalDict.get("ocsp") is not None):
                    #list of dictionaries
                    finalDict["ocsp"] = [finalDict["ocsp"] , value]
                else:
                    finalDict["ocsp"] = value

            if (key.startswith('crl_') and key.endswith('.crl')):
                if (finalDict.get("crl") is not None):
                    #list of dictionaries
                    finalDict["crl"] = [finalDict["crl"] , value]
                else:
                    finalDict["crl"] = value

            if (key.startswith('p12_') and key.endswith('.p12')):
                cuit = key.replace("p12_client-", "").replace(".p12", "")
                if (finalDict.get(cuit) is not None):
                    #list of dictionaries
                    finalDict[cuit] = [finalDict[cuit] , value]
                else:
                    finalDict[cuit] = value

            if (key.startswith('cer_') and key.endswith('.cer')):
                cuit = key.replace("cer_client-", "").replace(".cer", "")
                if (finalDict.get(cuit) is not None):
                    #list of dictionaries
                    finalDict[cuit] = [finalDict[cuit] , value]
                else:
                    finalDict[cuit] = value

        print("...update metadata with cvs file..")
        for registro in cvsDict:
            if (finalDict.get(registro["cuit"]) is not None):
                # agregamos nuevo elemento a la lista para el cuit en curso.
                finalDict[registro["cuit"]] = [finalDict[registro["cuit"]] ,{ 'data': {'cuit': registro["cuit"], 'email': registro["email"], 'razonSocial': registro["razonSocial"], 'localidad': registro["localidad"]}}]

        jsonPathFile = os.path.join(self.base_path, 'metadata.json')
        jsonCreated = serJson.dump(finalDict)
        serJson.saveJson(jsonPathFile, jsonCreated)

    def get_metadata(self):
        jsonPathFile = os.path.join(self.base_path, 'metadata.json')
        data = serJson.openJsonFile(jsonPathFile) #return a str
        return serJson.load(data, globals()) #return a dict
        
    def clean_metadata(self):
        """delete all files"""
        #borramos todos los archivos de nuestro repositorio
        for file in self.get_all_files():
            if (file.endswith('.crl')):
                cleanFolderForFile(file)
            if (file.endswith('.crt')):
                cleanFolderForFile(file)
            if (file.endswith('.key')):
                cleanFolderForFile(file)
            if (file.endswith('.cer')):
                cleanFolderForFile(file)
            if (file.endswith('.p12')):
                cleanFolderForFile(file)
            if (file.endswith('.json')):
                cleanFolderForFile(file)
            if (file.endswith('.pdf')):
                cleanFolderForFile(file)

    def exist_file(self, name):
        """check is exist the file name"""
        #chequeamos si existe el archivo en el repositorio
        for file in self.get_all_files():
            file_name = os.path.basename(file)
            if (name in file_name) or file_name.__contains__(name):
                return True
        return False

    def get_all_files(self, extension=None):
        """get list of all files"""
        #listamos todos los archivos. En caso de definir alguna extension, se filtra por ella.
        list = []
        files = certManager.getCertificates(self,self.base_path)
        for file in files:
            list.append(file)
        return list
