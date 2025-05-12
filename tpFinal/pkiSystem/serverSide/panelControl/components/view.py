# -*- coding: UTF-8 -*-
from tkinter import Toplevel, Label, Message
from components import frames, menu
from lib.functions import set_window_center
import lib.global_variable as glv
from pages import winAbout

#Helper para el tratamiento de los Frames a mostrar por cada menu.
class MainPage():

    def __init__(self, master=None):
        self.root = master
        
        set_window_center(self.root, 800, 600)
       
        menu.MainMenu(self)

        self.current_frame = None
        #He aqui la magia. Dict de Frame con su respectivas Key, Value:Class Frame
        self.page_frame = {
            "home": frames.HomeFrame,
            "documents_add": frames.DocumentAdd,
            "documents_list": frames.DocumentsList,
            "document_add_sign": frames.DocumentAddSign,
            "certificates_list": frames.CertificatesList,
            "contact": frames.AboutFrame
        }
        #Por cada metodo "open_*", se dispara una key del diccionario
        self.open_home()
        self.win_about = None
  
    #Metodo generico, con el cual abrimos cada frame
    def open_page(self, frame_name, title):
        self.root.title(title)
        #Si el frame cambia, debemos destruir el que esta en curso.
        if self.current_frame is not None and (hasattr(self.current_frame.destroy, '__call__')):
            self.current_frame.destroy()

        #buscamos el frame en nuestro diccionario y lo "dibujamos" sobre la ventana hija.
        self.current_frame = self.page_frame[frame_name](self.root)
        self.current_frame.pack()

    def open_home(self):
        self.open_page("home", "Interfaz principal de la aplicación")

    def open_documents_add(self):
        self.open_page("documents_add", "Carga de documento")

    def open_documents_list(self):
        self.open_page("documents_list", "Consulta de documentos")


    def open_document_add_sign(self):
        self.open_page("document_add_sign", "Firmar de documento")


    def open_cert_info(self):
        page = Toplevel()
        page.title("Detalles del certificado")
        page.resizable(False, False)
        
        set_window_center(page, 200, 150)

        Label(page, text="Nombre: ").grid(row=1, stick="w", pady=2)
        Label(page, text="administrador").grid(row=1, column=1, stick="e")

        Label(page, text="Cuenta: ").grid(row=2, stick="w", pady=2)
        Label(page, text="admin").grid(row=2, column=1, stick="e")

        Label(page, text="contraseña: ").grid(row=3, stick="w", pady=2)
        Label(page, text="admin").grid(row=3, column=1, stick="e")

    def open_cert_list(self):
        self.open_page("certificates_list", "Lista de Certificados")

    def open_about(self):
        """Acerca de las ventanas"""
        if self.win_about and self.win_about.destroy:
            self.win_about.destroy()
        self.win_about = winAbout.Init()



    def window_to_top(self):
        self.root.attributes('-topmost', True)

    def window_not_top(self):
        self.root.attributes('-topmost', False)
