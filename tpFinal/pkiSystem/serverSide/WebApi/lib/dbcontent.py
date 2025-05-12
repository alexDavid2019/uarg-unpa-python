# -*- coding: utf-8 -*-

from lib.sqlite_helper import DBHelper

def user_login(username, password) -> bool:
    if username is None or password is None:
        return False
    else:
        # session['username'] = name
        _db = DBHelper()
        if _db.has_user(username, password):
            return True
        else:
            return False


def user_list() -> list:
    _db = DBHelper()
    return _db.get_all_user_info()

def certificate_ca_list() -> list:
    _db = DBHelper()
    return _db.get_all_ca_info()

def certificate_ocsp_list() -> list:
    _db = DBHelper()
    return _db.get_all_ocsp_info()

def certificate_crl_list() -> list:
    _db = DBHelper()
    return _db.get_all_crl_info()

def certificate_list_by_username(username) -> list:
    _db = DBHelper()
    return _db.get_certificates_by_username(username)

def certificate_status_by_serialnumber(serialNumber) -> list:
    _db = DBHelper()
    return _db.get_certificate_status_by_serialnumber(serialNumber)

def certificate_list_by_username_certId(cuit, certId) -> list:
    _db = DBHelper()
    return _db.get_certificate_active_by_username_certId(cuit,certId)

def documents_list_by_username(cuit) -> list:
    _db = DBHelper()
    return _db.get_user_documents_by_username(cuit)

def documents_list_by_username_fileId(cuit,fileId) -> list:
    _db = DBHelper()
    return _db.get_user_documents_by_username_fileId(cuit,fileId)

def documents_list_by_username_filename(cuit,filename) -> list:
    _db = DBHelper()
    return _db.get_user_documents_by_username_filename(cuit,filename)

def save_documents_by_username(cuit, filePath) -> bool:
    _db = DBHelper()
    return _db.insert_document_by_username(cuit, filePath, 'pending')

def update_complete_document_by_username(cuit, fileId, pdfOuputPathFile) -> bool:
    _db = DBHelper()
    _db.update_document_status_by_username(cuit, 'completed', fileId)
    return _db.update_document_signed_by_username(cuit, pdfOuputPathFile, 1, fileId)

def pkcs12_active_by_username(cuit) -> list:
    _db = DBHelper()
    return _db.get_certificate_active_by_username(cuit)
