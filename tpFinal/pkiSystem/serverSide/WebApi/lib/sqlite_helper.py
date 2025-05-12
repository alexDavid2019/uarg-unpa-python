# -*- coding:utf-8-*-
import os
import datetime
import sqlite3
import lib.global_variable as glv

class DBHelper(object):
    """sqlite helper"""
    def __init__(self):
        self.db_path = os.path.join(glv.get_variable("DB_REPO_DIR"), 'database.db')
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
    
    def create_database(self):
        """create table"""
        self.cursor.execute('''create table IF NOT EXISTS ca(id INTEGER PRIMARY KEY, filename TEXT, iskey TEXT)''')
        self.cursor.execute('''create table IF NOT EXISTS ocsp(id INTEGER PRIMARY KEY, filename TEXT, iskey TEXT)''')
        self.cursor.execute('''create table IF NOT EXISTS crl(id INTEGER PRIMARY KEY, filename TEXT, iskey TEXT)''')
        
        self.cursor.execute('''create table IF NOT EXISTS user(id INTEGER PRIMARY KEY, cuit TEXT, description TEXT, email TEXT, localidad TEXT, password TEXT)''')
        self.cursor.execute('''create table IF NOT EXISTS user_certificate(id INTEGER, userid INTEGER, certificateid INTEGER)''')
        self.cursor.execute('''create table IF NOT EXISTS certificates(id INTEGER PRIMARY KEY, filename TEXT, type TEXT, status TEXT, serialNumber TEXT)''')
        self.cursor.execute('''create table IF NOT EXISTS user_documents(id INTEGER PRIMARY KEY, userid INTEGER, certificateid INTEGER, isSigned INTEGER, filename TEXT, status TEXT, fileSigned TEXT, updated TEXT, created TEXT)''')
        
        self.cursor.execute('''create unique index IF NOT EXISTS ca_unique_index on ca(filename)''')
        self.cursor.execute('''create unique index IF NOT EXISTS ocsp_unique_index on ocsp(filename)''')
        self.cursor.execute('''create unique index IF NOT EXISTS crl_unique_index on crl(filename)''')

        self.cursor.execute('''create unique index IF NOT EXISTS user_unique_index on user(cuit)''')
        self.cursor.execute('''create unique index IF NOT EXISTS user_certificate_unique_index on user_certificate(id)''')
        self.cursor.execute('''create unique index IF NOT EXISTS certificates_unique_index on certificates(filename)''')
        self.conn.commit()

    def reset_database(self):
        """drop table"""
        self.cursor.execute("DROP TABLE IF EXISTS ca")
        self.cursor.execute("DROP TABLE IF EXISTS ocsp")
        self.cursor.execute("DROP TABLE IF EXISTS crl")

        self.cursor.execute("DROP TABLE IF EXISTS user")
        self.cursor.execute("DROP TABLE IF EXISTS user_certificate")
        self.cursor.execute("DROP TABLE IF EXISTS user_documents")
        self.cursor.execute("DROP TABLE IF EXISTS certificates")
        self.conn.commit()
        self.create_database()

    def insert_ca_data(self, filename, iskey) -> bool:
        """insert ca data"""
        filename = filename.strip()
        info = filename, iskey
        try:
            self.cursor.execute('INSERT INTO ca(filename, iskey) VALUES(?, ?)', info)
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False
        

    def get_all_ca_info(self) -> list:
        """get list of all ca"""
        list = []
        rows = self.cursor.execute('SELECT id, filename, iskey FROM ca')
        for item in rows:
            list.append({
                'id': item[0],
                'filename': item[1],
                'iskey': item[2],
            })
        return list

    def insert_ocsp_data(self, filename, iskey) -> bool:
        """insert ocsp data"""
        filename = filename.strip()
        info = filename, iskey
        try:
            self.cursor.execute('INSERT INTO ocsp(filename, iskey) VALUES(?, ?)', info)
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False


    def get_all_ocsp_info(self) -> list:
        """get list of all ocsp"""
        list = []
        rows = self.cursor.execute('SELECT id, filename, iskey FROM ocsp')
        for item in rows:
            list.append({
                'id': item[0],
                'filename': item[1],
                'iskey': item[2],
            })
        return list


    def insert_crl_data(self, filename, iskey) -> bool:
        """insert crl data"""
        filename = filename.strip()
        info = filename, iskey
        try:
            self.cursor.execute('INSERT INTO crl(filename, iskey) VALUES(?, ?)', info)
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False


    def get_all_crl_info(self) -> list:
        """get list of all crl"""
        list = []
        rows = self.cursor.execute('SELECT id, filename, iskey FROM crl')
        for item in rows:
            list.append({
                'id': item[0],
                'filename': item[1],
                'iskey': item[2],
            })
        return list

    def insert_user_data(self, cuit, description, email, localidad, password) -> bool:
        """insert user"""
        cuit = cuit.strip()
        description = description.strip()
        password = password.strip()
        email = email.strip()
        localidad = localidad.strip()
        try:
            self.cursor.execute('INSERT INTO user(cuit, description, email, localidad, password) VALUES(?, ?, ?, ?, ?)', (cuit, description, email, localidad, password))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False

    def has_user(self, cuit, password) -> bool:
        """check user"""
        cuit = cuit.strip()
        password = password.strip()
        info = cuit, password
        flag = self.cursor.execute('SELECT * FROM user WHERE cuit=? and password=?', info).fetchall()
        if flag == []:
            return False
        else:
            return True

    def get_all_user_info(self) -> list:
        """get list of all user"""
        list = []
        rows = self.cursor.execute('SELECT id, cuit, description, email, localidad, password FROM user')
        for item in rows:
            list.append({
                'id': item[0],
                'cuit': item[1],
                'description': item[2],
                'email': item[3],
                'localidad': item[4],
                'password': item[5],
            })
        return list

    def insert_certificate_data(self, filename, type, status, serialNumber) -> bool:
        """insert certificate"""
        filename = filename.strip()
        type = type.strip()
        status = status.strip()
        try:
            self.cursor.execute('INSERT INTO certificates(filename, type, status, serialNumber) VALUES(?, ?, ?, ?)', (filename, type, status, serialNumber))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False

    def asociate_certificate_by_username(self, cuit, filename) -> bool:
        """relation with certificate by username"""
        try:
            userid = self.cursor.execute('SELECT id FROM user WHERE cuit=?', (cuit, )).fetchone()
            certificateid = self.cursor.execute('SELECT id FROM certificates WHERE filename=?', (filename, )).fetchone()
            
            count = self.cursor.execute('SELECT COUNT(*) FROM user_certificate').fetchone()
            rows = count[0]
            rows += 1
            self.cursor.execute('INSERT INTO user_certificate(id, userid, certificateid) VALUES (?, ?, ?)', (rows, userid[0], certificateid[0]))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False

    def get_all_asociate_info(self) -> list:
        """get list"""
        list = []
        rows = self.cursor.execute('SELECT id, userid, certificateid FROM user_certificate')
        for item in rows:
            list.append({
                'id': item[0],
                'userid': item[1],
                'certificateid': item[2],
            })
        return list
    
    def get_certificates_by_username(self, cuit) -> list:
        """get certificates list of user by username"""
        list = []
        userid = self.cursor.execute('SELECT id FROM user WHERE cuit=?', (cuit, )).fetchone()
        id = self.cursor.execute('SELECT id FROM user_certificate WHERE userid=?', userid).fetchall()
        for item in id:
            if item is not None:
                r = self.cursor.execute('SELECT id, filename, type, status, serialNumber FROM certificates WHERE id=?', item).fetchone()
                if r is not None:
                    list.append({
                        'id': r[0],
                        'filename': r[1],
                        'type': r[2],
                        'status': r[3],
                        'serialNumber': r[4]
                    })
        return list

    def get_certificate_active_by_username(self, cuit) -> list:
        """get one certificate by status and username """
        list = []
        row = self.cursor.execute('SELECT a.id, a.filename, a.type, a.status, a.serialNumber, u.cuit, u.description FROM certificates a inner join user_certificate b on b.certificateid = a.id inner join user u on u.id = b.userid where a.type = ? and a.status = ? and u.cuit = ?', ('.p12','active',cuit, )).fetchone()
        list.append({
            'id': row[0],
            'filename': row[1],
            'type': row[2],
            'status': row[3],
            'serialNumber': row[4],
            'cuit': row[5],
            'description': row[6]
        })
        return list

    def get_certificate_active_by_username_certId(self, cuit, certId) -> list:
        """get one certificate by status and username and Id """
        list = []
        row = self.cursor.execute('SELECT a.id, a.filename, a.type, a.status, a.serialNumber, u.cuit, u.description FROM certificates a inner join user_certificate b on b.certificateid = a.id inner join user u on u.id = b.userid where a.status = ? and u.cuit = ? and a.id = ?', ('active',cuit,certId, )).fetchone()
        list.append({
            'id': row[0],
            'filename': row[1],
            'type': row[2],
            'status': row[3],
            'serialNumber': row[4],
            'cuit': row[5],
            'description': row[6]
        })
        return list

    def get_certificate_status_by_serialnumber(self, serialNumber) -> list:
        """get one certificate by serial number"""
        list = []
        row = self.cursor.execute('SELECT a.id, a.filename, a.type, a.status, a.serialNumber, u.cuit, u.description FROM certificates a inner join user_certificate b on b.certificateid = a.id inner join user u on u.id = b.userid where a.serialNumber = ?', (serialNumber, )).fetchone()
        list.append({
            'id': row[0],
            'filename': row[1],
            'type': row[2],
            'status': row[3],
            'serialNumber': row[4],
            'cuit': row[5],
            'description': row[6]
        })
        return list

    def get_all_certificates(self) -> list:
        """get all certificates as list"""
        list = []
        rows = self.cursor.execute('SELECT a.id, a.filename, a.type, a.status, a.serialNumber, u.cuit, u.description FROM certificates a inner join user_certificate b on b.certificateid = a.id inner join user u on u.id = b.userid').fetchall()
        #rows = self.cursor.execute('SELECT a.id, a.filename, a.type, a.status FROM certificates a').fetchall()
        for item in rows:
            list.append({
                'id': item[0],
                'filename': item[1],
                'type': item[2],
                'status': item[3],
                'serialNumber': item[4],
                'cuit': item[5],
                'description': item[6]
            })
        return list

    def insert_document_by_username(self, cuit, document_Filename, status) -> bool:
        """insert data for user documents by username"""
        try:
            userid = self.cursor.execute('SELECT id FROM user WHERE cuit=?', (cuit, )).fetchone()
            certificateid = self.cursor.execute('SELECT a.certificateid FROM user_certificate a inner join certificates b on b.id = a.certificateid WHERE b.status = ? and b.type = ? and a.userid=?', ('active', '.p12', userid[0], )).fetchone()
            
            isSigned = 0
            created = datetime.datetime.now()
            self.cursor.execute('INSERT INTO user_documents(userid, certificateid, isSigned, filename, status, created ) VALUES (?, ?, ?, ?, ?, ?)', (userid[0], certificateid[0], isSigned, document_Filename, status, created))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False

    def update_document_status_by_username(self, cuit, status, fileId) -> bool:
        """update user documents by username"""
        try:
            userid = self.cursor.execute('SELECT id FROM user WHERE cuit=?', (cuit, )).fetchone()
            certificateid = self.cursor.execute('SELECT a.certificateid FROM user_certificate a inner join certificates b on b.id = a.certificateid WHERE b.status = ? and b.type = ? and a.userid=?', ('active', '.p12', userid[0], )).fetchone()
            
            updated = datetime.datetime.now()
            self.cursor.execute('UPDATE user_documents set status = ?, updated = ? where userid = ? and certificateid = ? and id = ?', (status, updated, userid[0], certificateid[0], fileId, ))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False


    def update_document_signed_by_username(self, cuit, pdfOuputPathFile, isSigned, fileId) -> bool:
        """update user documents by username"""
        try:
            userid = self.cursor.execute('SELECT id FROM user WHERE cuit=?', (cuit, )).fetchone()
            certificateid = self.cursor.execute('SELECT a.certificateid FROM user_certificate a inner join certificates b on b.id = a.certificateid WHERE b.status = ? and b.type = ? and a.userid=?', ('active', '.p12', userid[0], )).fetchone()
            
            updated = datetime.datetime.now()
            self.cursor.execute('UPDATE user_documents set isSigned = ?, fileSigned = ?, updated = ? where userid = ? and certificateid = ? and id = ?', (isSigned, pdfOuputPathFile, updated, userid[0], certificateid[0], fileId, ))
            self.conn.commit()
            return True
        except Exception as err:
            print(err)
            return False

    def get_user_documents_by_username(self, cuit) -> list:
        """get all user documents as list"""
        list = []
        rows = self.cursor.execute('SELECT a.id, a.isSigned, a.filename, a.status, a.fileSigned, a.updated, a.created, u.cuit, u.description FROM user_documents a inner join user u on u.id = a.userid where u.cuit = ?',(cuit, )).fetchall()
        for item in rows:
            list.append({
                'id': item[0],
                'isSigned': item[1],
                'filename': item[2],
                'status': item[3],
                'fileSigned': item[4],
                'updated': item[5],
                'created': item[6],
                'cuit': item[7],
                'description': item[8],
                'base64File':''
            })
        return list


    def get_user_documents_by_username_fileId(self, cuit, fileId) -> list:
        """get all user documents as list"""
        list = []
        rows = self.cursor.execute('SELECT a.id, a.isSigned, a.filename, a.status, a.fileSigned, a.updated, a.created, u.cuit, u.description FROM user_documents a inner join user u on u.id = a.userid where u.cuit = ? and a.id = ?',(cuit, fileId, )).fetchall()
        for item in rows:
            list.append({
                'id': item[0],
                'isSigned': item[1],
                'filename': item[2],
                'status': item[3],
                'fileSigned': item[4],
                'updated': item[5],
                'created': item[6],
                'cuit': item[7],
                'description': item[8],
                'base64File':''
            })
        return list
    
    
    def get_user_documents_by_username_filename(self, cuit, filename) -> list:
        """get all user documents as list"""
        list = []
        rows = self.cursor.execute('SELECT a.id, a.isSigned, a.filename, a.status, a.fileSigned, a.updated, a.created, u.cuit, u.description FROM user_documents a inner join user u on u.id = a.userid where u.cuit = ? and a.filename = ?',(cuit, filename, )).fetchall()
        for item in rows:
            list.append({
                'id': item[0],
                'isSigned': item[1],
                'filename': item[2],
                'status': item[3],
                'fileSigned': item[4],
                'updated': item[5],
                'created': item[6],
                'cuit': item[7],
                'description': item[8],
                'base64File':''
            })
        return list
    
    def get_all_user_documents(self) -> list:
        """get all user documents as list"""
        list = []
        rows = self.cursor.execute('SELECT a.id, a.isSigned, a.filename, a.status, a.fileSigned, a.updated, a.created, u.cuit, u.description FROM user_documents a inner join user u on u.id = a.userid').fetchall()
        for item in rows:
            list.append({
                'id': item[0],
                'isSigned': item[1],
                'filename': item[2],
                'status': item[3],
                'fileSigned': item[4],
                'updated': item[5],
                'created': item[6],
                'cuit': item[7],
                'description': item[8],
                'base64File':''
            })
        return list
