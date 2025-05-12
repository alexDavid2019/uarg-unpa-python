# -*- coding: UTF-8 -*-
import os
import base64
import subprocess
import tempfile

from PIL import Image, ImageTk

from tkinter import (Button, Label, Text, Frame, Entry, LabelFrame, StringVar, messagebox,
                     scrolledtext, filedialog, ttk)

from lib.request_helper import RequestHelper as reqHelper

import lib.global_variable as glv
from lib.functions import treeview_sort_column

#Clase de tipo FRAME
class HomeFrame(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        self.init_page()
        #self.set_image_background()

    def init_page(self):
        Label(self, text="*** Usuario Autenticado ***").pack()
        Label(self, text="Usuario " + str(glv.get_variable("CURRENT_USER_NAME"))).pack()
        Button(self, text="Salir",command=self.root.quit).pack()

    def set_image_background(self):
        image_file = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "image",
            "pki-logo.png",
        )
        img  = ImageTk.PhotoImage(file = image_file)
        bg_image = Label(self,image=img)
        bg_image.place(relwidth=1, relheight=1)
        #Inyectamos un label a pie de pantalla
        #Label(self, text="PKI SYSTEM", bg="green", fg="#fff", height=2).pack(
        #    fill="both", side="bottom"
        #)

#Clase de tipo FRAME
class DocumentAdd(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        self.selected_filePath = StringVar()
        self.control_label_filePath = Label
        self.init_page()

    def init_page(self):
        Label(self).grid(row=0, stick="w", pady=10)

        lb1 = Label(self, text="Seleccione un archivo PDF a enviar: ")
        lb1.grid(row=1, stick="w", pady=10)

        bt1 = Button(self, text="Abrir", command=self.__do_open_file)
        bt1.grid(row=1, column=1, stick="E", pady=10)

        lb2 = Label(self, text="Archivo: ")
        lb2.grid(row=3, stick="W", pady=10)

        path_label = Label(self, text="..........")
        path_label.grid(row=3, column=1, columnspan=2, stick="E")
        self.control_label_filePath = path_label

        bt1 = Button(self, text="Enviar archivo seleccionado.", command=self.do_add)
        bt1.grid(row=4, column=1, columnspan=3, stick="E", pady=10)

    def __do_open_file(self):
        self.selected_filePath = filedialog.askopenfilename(
            initialdir=".",
            title="Select a file",
            filetypes=(("Pdf files", "*.pdf"), ("All files", "*.*"))
        )
        #messagebox.showinfo("Abrir Archivo", f"Usted selecciono un archivo : {self.selected_filePath}") 
        self.control_label_filePath.config(text=self.selected_filePath)

    def do_add(self):
         #Para el usuario en curso, buscamos la info correspondiente
        username = str(glv.get_variable("CURRENT_USER_NAME"))
        res = reqHelper.document_add_by_user(reqHelper, username, self.__pdf_to_base64(self.selected_filePath))
        if res is True:
            messagebox.showinfo(title="Aviso", message="Archivo enviado con exito.")
        else:
            messagebox.showinfo(title="Aviso", message="No es posible enviar el archivo.")

    def __pdf_to_base64(self, pdf_path):
        """
        Converts a PDF file to a Base64 string.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The Base64 encoded string of the PDF file, or None if an error occurs.
        """
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                base64_bytes = base64.b64encode(pdf_bytes)
                base64_string = base64_bytes.decode("ascii")
                return base64_string
        except FileNotFoundError:
            print(f"Error: File not found at path: {pdf_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None



#Clase de tipo FRAME
class DocumentAddSign(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        self.selected_filePath = StringVar()
        self.control_label_filePath = Label
        self.init_page()

    def init_page(self):
        Label(self).grid(row=0, stick="w", pady=10)

        lb1 = Label(self, text="Seleccione un archivo PDF a FIRMAR: ")
        lb1.grid(row=1, stick="w", pady=10)

        bt1 = Button(self, text="Abrir", command=self.__do_open_file)
        bt1.grid(row=1, column=1, stick="E", pady=10)

        lb2 = Label(self, text="Archivo: ")
        lb2.grid(row=3, stick="W", pady=10)

        path_label = Label(self, text="..........")
        path_label.grid(row=3, column=1, columnspan=2, stick="E")
        self.control_label_filePath = path_label

        bt1 = Button(self, text="Firmar archivo seleccionado.", command=self.do_add_sign)
        bt1.grid(row=4, column=1, columnspan=3, stick="E", pady=10)

    def __do_open_file(self):
        self.selected_filePath = filedialog.askopenfilename(
            initialdir=".",
            title="Select a file",
            filetypes=(("Pdf files", "*.pdf"), ("All files", "*.*"))
        )
        #messagebox.showinfo("Abrir Archivo", f"Usted selecciono un archivo : {self.selected_filePath}") 
        self.control_label_filePath.config(text=self.selected_filePath)

    def do_add_sign(self):
         #Para el usuario en curso, buscamos la info correspondiente
        username = str(glv.get_variable("CURRENT_USER_NAME"))
        res = reqHelper.document_add_sign_by_user(reqHelper, username, self.__pdf_to_base64(self.selected_filePath))
        if res is True:
            messagebox.showinfo(title="Aviso", message="Archivo firmado con exito.")
        else:
            messagebox.showinfo(title="Aviso", message="No es posible firmar el archivo.")

    def __pdf_to_base64(self, pdf_path):
        """
        Converts a PDF file to a Base64 string.

        Args:
            pdf_path (str): The path to the PDF file.

        Returns:
            str: The Base64 encoded string of the PDF file, or None if an error occurs.
        """
        try:
            with open(pdf_path, "rb") as pdf_file:
                pdf_bytes = pdf_file.read()
                base64_bytes = base64.b64encode(pdf_bytes)
                base64_string = base64_bytes.decode("ascii")
                return base64_string
        except FileNotFoundError:
            print(f"Error: File not found at path: {pdf_path}")
            return None
        except Exception as e:
            print(f"An error occurred: {e}")
            return None
        
#Clase de tipo FRAME
class DocumentsList(Frame):
    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        
        self.list = []
        self.selected_item = None
        self.selected_name = StringVar()
        self.selected_id = StringVar()
        self.selected_status = StringVar()
        self.win_content_info = None
        self.win_content_edit = None
        self.init_page()

    def init_page(self):
        #Para el usuario en curso, buscamos la info correspondiente
        username = str(glv.get_variable("CURRENT_USER_NAME"))
        #recuperamos los documentos pendientes o ya firmados desde el server.
        self.list = reqHelper.documents_by_user(reqHelper, username)

        head_frame = LabelFrame(self, text=f"Documentos del usuario {username}")

        #Posibles valores del attr sticky con el cual alineamos la celda.        
        #sticky='' (default): The widget is centered within the cell.
        #sticky='N': The widget is aligned to the top of the cell.
        #sticky='S': The widget is aligned to the bottom of the cell.
        #sticky='E': The widget is aligned to the right of the cell.
        #sticky='W': The widget is aligned to the left of the cell. 
        #sticky='NE': The widget is aligned to the top-right corner of the cell.
        #sticky='NW': The widget is aligned to the top-left corner of the cell.
        #sticky='SE': The widget is aligned to the bottom-right corner of the cell.
        #sticky='SW': The widget is aligned to the bottom-left corner of the cell.
        #sticky='NS': The widget is stretched vertically to fill the height of the cell.
        #sticky='EW': The widget is stretched horizontally to fill the width of the cell.
        #sticky='NSEW': The widget is stretched to fill the entire cell, both horizontally and vertically

        #head_frame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        head_frame.grid(row=0, column=0, sticky="NSEW")

        Label(head_frame, textvariable=self.selected_name).pack()

        btn_info = Button(head_frame, text="Mostrar documento", command=self.info)
        btn_info.pack(side="left")
        btn_sign = Button(head_frame, text="Firmar documento", command=self.do_sign)
        btn_sign.pack(side="left")
        btn_refresh = Button(head_frame, text="Refrescar listado", command=self.do_refresh)
        btn_refresh.pack(side="left")

        self.tree_view = ttk.Treeview(self, show="headings")

        self.tree_view["columns"] = ("id", "status", "filename", "isSigned", "created")
    
        self.tree_view.column("id", width=25)
        self.tree_view.column("status", width=60)
        self.tree_view.column("filename", width=120)
        self.tree_view.column("isSigned", width=25)
        self.tree_view.column("created", width=100)
    
        self.tree_view.heading("id", text="ID")
        self.tree_view.heading("status", text="ESTADO")
        self.tree_view.heading("filename", text="ARCHIVO")
        self.tree_view.heading("isSigned", text="Firmado?")
        self.tree_view.heading("created", text="FECHA")

        num = 1
        for item in self.list:
            filename = item["filename"]
            firmado = "No"
            if (str(item["isSigned"]) == "1"):
                filename = item["fileSigned"]
                firmado = "Si"
            filename = filename.split('\\')[-1]
            self.tree_view.insert(
                "",
                num,
                text="",
                values=(item["id"], item["status"], filename, firmado, item["created"]),
            )

        self.tree_view.bind("<<TreeviewSelect>>", self.select)

        for col in self.tree_view["columns"]:
            self.tree_view.heading(
                col,
                text=col,
                command=lambda _col=col: treeview_sort_column(
                    self.tree_view, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
        
        self.tree_view.configure(yscrollcommand=vbar.set)
        
        self.tree_view.grid(row=1, column=0, sticky="NSEW")
        #self.tree_view.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        vbar.grid(row=1, column=1, sticky="NS")

    def select(self, event):

        slct = event.widget.selection()[0]
        self.selected_item = self.tree_view.item(slct)

        self.selected_id.set(self.selected_item["values"][0])
        self.selected_status.set(self.selected_item["values"][1])

        #print("you clicked on ", self.selected_item)

    def do_refresh(self):
        for item in self.tree_view.get_children():
            self.tree_view.delete(item)

        num = 1
        for item in self.list:
            filename = item["filename"]
            firmado = "No"
            if (str(item["isSigned"]) == "1"):
                filename = item["fileSigned"]
                firmado = "Si"
            filename = filename.split('\\')[-1]
            self.tree_view.insert(
                "",
                num,
                text="",
                values=(item["id"], item["status"], filename, firmado, item["created"]),
            )
        self.tree_view.bind_all()
        
    def info(self):
        
        if self.selected_item is None:
            messagebox.showinfo("Aviso", "Es necesario seleccionar un item")
        else:
            if self.win_content_info is not None and hasattr(self.win_content_info.destroy, "__call__"):
                # if self.win_content_info and self.win_content_info.destroy:
                self.win_content_info.destroy()

            username = str(glv.get_variable("CURRENT_USER_NAME"))
            docId = str(self.selected_item["values"][0])
            jsonResultData = reqHelper.document_by_user_certId(reqHelper, username, docId)

            if (jsonResultData is None):
                messagebox.showinfo("No se puede recuperar el documento del tipo PDF en este momento.", self.selected_item)
                return

            self.__show_pdf(jsonResultData[0]["base64File"])
    
    #Metodo privado
    def __show_pdf(self, base64_data):
        """
        Decodes a base64 string and displays it as a PDF using an external viewer.

        Args:
            base64_string: The base64 encoded PDF data.
        """
        try:

            decoded_bytes = base64.b64decode(base64_data)
             
            # Create a named temporary file
            with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmpfile:
                # Write to the file
                tmpfile.write(decoded_bytes)
                tmpfile.flush()  # Ensure the data is written to the file
                # Get the file name
                file_name = tmpfile.name
                #print(f"Temporary file name: {file_name}")

                # Verify the file exists
                #print(f"File exists before closing: {os.path.exists(file_name)}")

                # Close the temporary file
                tmpfile.close()

            if os.name == 'nt':
                os.startfile(file_name)
            elif os.name == 'posix':
                subprocess.Popen(['xdg-open', file_name])
            else:
                print("Unsupported operating system for opening PDF.")
        except Exception as e:
            print(f"Error displaying PDF: {e}")
        


    def do_sign(self):

        if self.selected_item is None:
            messagebox.showinfo("Aviso", "Es necesario seleccionar un item")
            return
            
        #isSigned == 1
        if (self.selected_item["values"][3] == "1"):
            messagebox.showinfo("Documento ya esta firmado. Solo requiere de una firma.", self.selected_item)
            return

        #Para el usuario en curso, buscamos la info correspondiente
        username = str(glv.get_variable("CURRENT_USER_NAME"))
        fileId = str(self.selected_id.get())
        res = reqHelper.document_sign_by_id(reqHelper, username, fileId)
        if res is True:
            #recuperamos los documentos pendientes o ya firmados desde el server.
            self.list = reqHelper.documents_by_user(reqHelper, username)
            messagebox.showinfo(title="Aviso", message="Archivo firmado con exito. Por favor, refresque la pantalla.")
        else:
            messagebox.showinfo(title="Aviso", message="No es posible firmar el archivo.")


#Clase de tipo FRAME
class CertificatesList(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        self.list = []
        self.selected_item = None
        self.selected_id = StringVar()
        self.selected_name = StringVar()
        self.win_content_info = None
        self.init_page()

    def init_page(self):
        #Para el usuario en curso, buscamos la info correspondiente
        username = str(glv.get_variable("CURRENT_USER_NAME"))
        #recuperamos los certificados desde el server.
        self.list = reqHelper.certificates_by_user(reqHelper, username)

        head_frame = LabelFrame(self, text=f"Certificados del usuario {username}")

        #Posibles valores del attr sticky con el cual alineamos la celda.        
        #sticky='' (default): The widget is centered within the cell.
        #sticky='N': The widget is aligned to the top of the cell.
        #sticky='S': The widget is aligned to the bottom of the cell.
        #sticky='E': The widget is aligned to the right of the cell.
        #sticky='W': The widget is aligned to the left of the cell. 
        #sticky='NE': The widget is aligned to the top-right corner of the cell.
        #sticky='NW': The widget is aligned to the top-left corner of the cell.
        #sticky='SE': The widget is aligned to the bottom-right corner of the cell.
        #sticky='SW': The widget is aligned to the bottom-left corner of the cell.
        #sticky='NS': The widget is stretched vertically to fill the height of the cell.
        #sticky='EW': The widget is stretched horizontally to fill the width of the cell.
        #sticky='NSEW': The widget is stretched to fill the entire cell, both horizontally and vertically

        #head_frame.grid(row=0, column=0, columnspan=2, sticky="NSEW")
        head_frame.grid(row=0, column=0, sticky="NSEW")

        Label(head_frame, textvariable=self.selected_name).pack()

        btn_info = Button(head_frame, text="Mostrar Certificado", command=self.info)
        btn_info.pack(side="left")
    
        self.tree_view = ttk.Treeview(self, show="headings")

        self.tree_view["columns"] = ("id", "status", "filename", "type", "serialNumber")
    
        self.tree_view.column("id", width=25)
        self.tree_view.column("status", width=100)
        self.tree_view.column("filename", width=100)
        self.tree_view.column("type", width=25)
        self.tree_view.column("serialNumber", width=100)
    
        self.tree_view.heading("id", text="ID")
        self.tree_view.heading("status", text="ESTADO")
        self.tree_view.heading("filename", text="ARCHIVO")
        self.tree_view.heading("type", text="TIPO")
        self.tree_view.heading("serialNumber", text="S.N.")

        num = 1
        for item in self.list:
            self.tree_view.insert(
                "",
                num,
                text="",
                values=(item["id"], item["status"], item["filename"], item["type"], item["serialNumber"]),
            )

        self.tree_view.bind("<<TreeviewSelect>>", self.select)

        for col in self.tree_view["columns"]:
            self.tree_view.heading(
                col,
                text=col,
                command=lambda _col=col: treeview_sort_column(
                    self.tree_view, _col, False
                ),
            )

        vbar = ttk.Scrollbar(self, orient="vertical", command=self.tree_view.yview)
        
        self.tree_view.configure(yscrollcommand=vbar.set)
        
        self.tree_view.grid(row=1, column=0, sticky="NSEW")
        #self.tree_view.grid(row=1, column=0, columnspan=3, padx=5, pady=5)

        vbar.grid(row=1, column=1, sticky="NS")

    def select(self, event):

        slct = event.widget.selection()[0]
        self.selected_item = self.tree_view.item(slct)

        self.selected_id.set(self.selected_item["values"][0])
        
        #print("you clicked on ", self.selected_item)

    def info(self):
        
        if self.selected_item is None:
            messagebox.showinfo("Aviso", "Es necesario seleccionar un item")
        else:
            if self.win_content_info is not None and hasattr(self.win_content_info.destroy, "__call__"):
                # if self.win_content_info and self.win_content_info.destroy:
                self.win_content_info.destroy()

            #type == .cer
            if (self.selected_item["values"][3] != ".cer"):
                messagebox.showinfo("Solo es posible ver certificado del tipo x509 DER.", self.selected_item)
                return

            username = str(glv.get_variable("CURRENT_USER_NAME"))
            certId = str(self.selected_item["values"][0])
            x509Data = reqHelper.certificate_by_user_certId(reqHelper, username,certId)
            if (x509Data is None):
                messagebox.showinfo("No es recuperar el certificado del tipo x509 DER en este momento.", self.selected_item)
                return

            self.__show_certificate(x509Data)

    #Metodo privado
    def __show_certificate(self, base64_bytes):
        try:

            #decoded_string = base64_bytes.decode('utf-8')

            # Create a named temporary file
            with tempfile.NamedTemporaryFile(suffix='.cer', delete=False) as tmpfile:
                # Write to the file
                tmpfile.write(base64_bytes)
                tmpfile.flush()  # Ensure the data is written to the file
                # Get the file name
                file_name = tmpfile.name
                #print(f"Temporary file name: {file_name}")

                # Verify the file exists
                #print(f"File exists before closing: {os.path.exists(file_name)}")

                if os.name == 'nt':
                    os.startfile(file_name)
                elif os.name == 'posix':
                    subprocess.Popen(['xdg-open', file_name])
                else:
                    print("Unsupported operating system for opening PDF.")

        except Exception as e:
            print(f"Error displaying certificate: {e}")

#Clase de tipo FRAME
class AboutFrame(Frame):

    def __init__(self, parent=None):
        Frame.__init__(self, parent)
        self.root = parent
        self.init_page()

    def init_page(self):
        Label(self, text="mensage").grid()
        Label(self, text="Similar a una ventana emergente, tiene propiedades de ventana independientes.", width=150).grid()


