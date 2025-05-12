# -*- coding: UTF-8 -*-

from tkinter import Menu, messagebox, filedialog

#Helper para centralizar el tratamiento de los menues.
class MainMenu:

    def __init__(self, master):
        self.master = master
        #Del padre obtenemos la ventana hija
        self.root = master.root
        self.init_menu()

    def init_menu(self):
        #Sobre la ventana hija, inyectamos los menues
        self.menubar = Menu(self.root)

        self.root.config(menu=self.menubar)
        
        filemenu = Menu(self.menubar, tearoff=0)
        #Por cada menu, definimos el evento apropiado
        filemenu.add_command(label="Abrir PDF", command=self.file_open)
        filemenu.add_separator()
        filemenu.add_command(label="Salir", command=self.root.quit)

        certificatesMenu = Menu(self.menubar, tearoff=0)
        certificatesMenu.add_command(label="Listar Certificados", command=self.master.open_cert_list)

        documentsMenu = Menu(self.menubar, tearoff=0)
        documentsMenu.add_command(label="Listar Documentos", command=self.master.open_documents_list)
        documentsMenu.add_command(label="Cargar Nuevo Documento", command=self.master.open_documents_add)
        documentsMenu.add_command(label="Cargar y Firmar Documento", command=self.master.open_document_add_sign)
            
        window_menu = Menu(self.menubar)
        window_menu.add_command(label="Acerca de", command=self.win_about)
        window_menu.add_separator()
        window_menu.add_command(label="Home", command=self.master.open_home)

        self.menubar.add_cascade(label="File", menu=filemenu)
        self.menubar.add_cascade(label="Certificados", menu=certificatesMenu)
        self.menubar.add_cascade(label="Documentos", menu=documentsMenu)
        self.menubar.add_cascade(label="Window", menu=window_menu)


    def file_open(self):
        file_path = filedialog.askopenfilename(
            initialdir=".",
            title="Select a file",
            filetypes=(("Pdf files", "*.pdf"), ("All files", "*.*"))
        )
        messagebox.showinfo("Abrir Archivo", f"Usted selecciono un archivo : {file_path}") 

    def win_about(self):
        messagebox.showinfo(
            "Acerca de..", "Simulacion de un Sistema PKI, del lado cliente."
        )
