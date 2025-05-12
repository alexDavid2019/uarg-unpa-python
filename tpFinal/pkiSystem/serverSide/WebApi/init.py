# -*- coding:utf-8-*-

import os
from lib.sqlite_helper import DBHelper
from lib.certs_helper import CERHelper

import lib.global_variable as glv

# Load global variable management module
glv.init_global_variable()
glv.set_variable("APP_NAME", "Application")
glv.set_variable("APP_PATH", os.path.dirname(__file__))
glv.set_variable("DATA_DIR", os.path.join(glv.get_variable("APP_PATH"), "data"))
glv.set_variable("DB_REPO_DIR",  os.path.join(glv.get_variable("DATA_DIR"), "dbRepository"))
glv.set_variable("FILES_REPO_DIR",  os.path.join(glv.get_variable("DATA_DIR"), "fileRepository"))

def do_init_system():
    db_helper = DBHelper()
    cer_helper = CERHelper()
    try:
        cer_helper.clean_metadata()
        db_helper.reset_database()

        #crea certificados y json con la metadata de clientes.
        cer_helper.create_metadata()
        db_helper.create_database()

        json_object = cer_helper.get_metadata()

        for key, value in json_object.items(): #Returns key-value pairs

            if (key =="ca"):
                #print(type(value)) #<class 'list'>
                for item in value:
                    #print(type(item)) #<class 'dict'>
                    db_helper.insert_ca_data(item["file_name"],item["file_name_iskey"])

            if (key =="ocsp"):
                #print(type(value)) #<class 'list'>
                for item in value:
                    #print(type(item)) #<class 'dict'>
                    db_helper.insert_ocsp_data(item["file_name"],item["file_name_iskey"])

            if (key =="crl"):
                #print(value)
                #print(type(value)) #<class 'dict'>
                db_helper.insert_crl_data(value["file_name"],value["file_name_iskey"])
            
            if (key !="ca" and key !="ocsp"):
                #print(type(value)) #<class 'list'>
                #primero insertamos usuariosel usuario.
                cuit=''
                for item in value:
                    if isinstance(item, dict):
                        cuit=item["data"]["cuit"]
                        tempDataUser = db_helper.insert_user_data(item["data"]["cuit"], item["data"]["razonSocial"], item["data"]["email"], item["data"]["localidad"], item["data"]["cuit"])
                #segundo insertamos los certificados asociados.
                for items in value:
                    if isinstance(items, list):
                        for item in items:
                            archivo = item["file_name"]
                            db_helper.insert_certificate_data(archivo,item["file_extension"], "active", item["serialNumber"])
                            db_helper.asociate_certificate_by_username(cuit,archivo)
        #check data
        #tempCA = db_helper.get_all_ca_info()
        #print(tempCA)
        #tempOcsp = db_helper.get_all_ocsp_info()
        #print(tempOcsp)
        #tempUser = db_helper.get_all_user_info();
        #print(tempUser)
        #tempData = db_helper.get_all_asociate_info()
        #print(tempData)
        tempData = db_helper.get_all_certificates();
        if (tempData is not None):
            print("--- sistema inicializado ---")
            
    except KeyError as e:
        print(e)

if __name__ == "__main__":
    do_init_system()
