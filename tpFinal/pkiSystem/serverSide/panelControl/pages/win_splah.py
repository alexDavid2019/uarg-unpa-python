# -*- coding: UTF-8 -*-

import os
from tkinter import Canvas, Label, Tk
from PIL import Image, ImageTk

import lib.global_variable as glv
from lib.functions import set_window_center

class Splah(Tk):
    #Constructor
    def __init__(self):
        #Simil a super() de java
        Tk.__init__(self)
        self.title("Splah...")
        #definimos coordenadas donde mostrar nuestra ventana
        self.w = 300
        self.h = 300
        set_window_center(self, self.w, self.h)
        self.resizable(False, False)
        #Dibujamos el contenido en la misma ventana.
        self.splash()

    def splash(self):
        #Dibujamos un Canvas en pantalla con fondo blanco
        #canvas = Canvas(self, width=self.w, height=250, bg="white")
        #canvas.create_text(
        #    self.w / 2, 250 / 2, text="PKI SYSTEM", font="time 20", tags="string"
        #)
        #canvas.pack(fill="both")
        
        #Inyectamos un fondo de pantalla en lugar del Canvas
        image_file = os.path.join(
            glv.get_variable("APP_PATH"),
            glv.get_variable("DATA_DIR"),
            "image",
            "pki-logo-220x161.png",
        )
        img  = ImageTk.PhotoImage(file = image_file)
        bg_image = Label(self,image=img)
        bg_image.place(relwidth=1, relheight=0.9)
        #Inyectamos un label a pie de pantalla
        Label(self, text="PKI SYSTEM", bg="green", fg="#fff", height=2).pack(
            fill="both", side="bottom"
        )

        #La temporizacion esta definida por 4seg y luego se destruye la instancia  
        self.after(4000, self.destroy)

        self.mainloop()
