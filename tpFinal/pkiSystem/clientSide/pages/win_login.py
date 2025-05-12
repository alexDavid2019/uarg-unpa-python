# -*- coding: UTF-8 -*-

from tkinter import Button, Entry, Frame, Label, Menu, StringVar, messagebox

from lib.request_helper import RequestHelper as reqHelper
import lib.global_variable as glv
from components.view import MainPage
from lib.functions import set_window_center

class Login():
    #Constructor
    def __init__(self, master=None):
        #En caso de que el usuario ya fue logeado con exito, no necesito mostrar Login
        if self.isLoggedIn() is True:
            #Inicializamos Clase contenedora de Marcos
            MainPage(master)
        else:
            self.root = master
            self.root.title("Login")
            set_window_center(self.root, 300, 180)
            #Recibe el valor de las "Entradas" asociadas a los controles labels.
            self.username = StringVar()
            self.password = StringVar()
            self.init_menu()
            self.init_page()

    def init_page(self):
        #cremos un attr page del tipo Frame inicializado con el window padre
        self.page = Frame(self.root)
        self.page.pack()
        #Tratamos todos los controles como grilla en el contenedor para facilitar la geometria
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

        #Dibujamos los controles en sus correspondientes celdas.
        Label(self.page).grid(row=0, stick="W")

        Label(self.page, text="Usuario : ").grid(row=1, stick="W", pady=10)
        username = Entry(self.page, textvariable=self.username)
        username.grid(row=1, column=1, stick="E")
        #usamos la funcion bind para capturar los eventos. En este caso, el retorno se realiza sobre la misma var.
        username.bind("<Return>", self.returnEnvent)

        Label(self.page, text="Password : ").grid(row=2, stick="W", pady=10)
        password = Entry(self.page, textvariable=self.password, show="*")
        password.grid(row=2, column=1, stick="E")
        #usamos la funcion bind para capturar los eventos. En este caso, el retorno se realiza sobre la misma var.
        password.bind("<Return>", self.returnEnvent)

        #El evento click del boton, ejecutara una funcion local
        button_login = Button(self.page, text="Login", command=self.doLogin)
        button_login.grid(row=3, column=1, stick="W", pady=10)
        #El evento click del boton, ejecutara una funcion local
        button_cancel = Button(self.page, text="Cancelar", command=self.doCancel)
        button_cancel.grid(row=3, column=1, stick="E")

    def init_menu(self):
        menubar = Menu(self.root)
        #Inyectamos un pequeño Menu a la ventana
        filemenu = Menu(menubar, tearoff=0)
        filemenu.add_command(label="Salir", command=self.root.quit)
        menubar.add_cascade(label="Menu", menu=filemenu)
        self.root.config(menu=menubar)

    def doLogin(self):
        #Desde los controles ENTRY se recupera el contenido hacia dos variables
        username = self.username.get()
        password = self.password.get()
        #Desde nuestro helper, invocamos los requests a la API
        is_ok, message = reqHelper.user_login(reqHelper, username, password)
        if is_ok is True:
            #Si la info es correcta, se destruye este window
            self.page.destroy()
            #Inicializamos var globales.
            glv.set_variable("CURRENT_USER_NAME", str(username))
            MainPage(self.root)
        else:
            #Si la info no es correcta, mostramos popup
            messagebox.showinfo(title="Aviso", message=f"Login fallido: {message}")

    def doCancel(self):
        glv.set_variable("CURRENT_USER_NAME", None)
        self.page.quit()

    def returnEnvent(self, event):
        self.doLogin()

    def isLoggedIn(self):
        return glv.get_variable("CURRENT_USER_NAME") is not None
