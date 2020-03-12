import tkinter as tk
from tkinter import ttk
from urllib.request import urlopen
from bs4 import BeautifulSoup 
import mysql.connector as mysql
from tkinter import messagebox as Messagebox


def analisis():
    global base 
    base=""
    conexion = mysql.connect( host='localhost', user= 'root', passwd='', db='a_pagina' )
    sql="insert into paginas(Pagina, status) values (%s,%s)"
    operacion = conexion.cursor()
    url = urlopen(paginaC.get())
    bs = BeautifulSoup(url.read(), 'html.parser')
    for enlaces in bs.find_all("a"):
        pag = "{}".format(enlaces.get("href"))
        datos=(pag, False)
        operacion.execute(sql, datos)
        conexion.commit
    operacion.execute( "SELECT * FROM paginas" )
    for Pagina, status in operacion.fetchall() :
        if(status==0):
            print(Pagina)
            url = urlopen(Pagina)
            base += "      --" + Pagina + "\n"
            bs1 = BeautifulSoup(url.read(), 'html.parser')
            for enlaces in bs1.find_all("a"):
                pag1 = "{}".format(enlaces.get("href"))
                base += "{}".format(enlaces.get("href"))
                base += "\n"
                datos=(pag1, True)
                operacion.execute(sql, datos)
                conexion.commit
            print("\nFin de enlaces encontrados\n")
    operacion.execute("update paginas set status=1 where status=0")
    conexion.commit   
    conexion.close()
    
    accion1.configure(state='enable')
def Bd():
    ventana1=tk.Tk()
    ventana1.title("Paginas Analizadas")
    texto11= ttk.Label(ventana1, text=base )
    texto11.grid(column=0,row=0)
    
   



    
   

ventana=tk.Tk()
ventana.title("Practica 3")
texto1= ttk.Label(ventana, text="URL: ")
texto1.grid(column=0,row=2)
pagina = tk.StringVar()
paginaC = ttk.Entry(ventana, width=34, textvariable=pagina)
paginaC.grid(column=1,row=2, columnspan=3)
accion = ttk.Button(ventana,text="Analizar pagina", command = analisis)
accion.grid(column=3,row=4)
accion1 = ttk.Button(ventana,text="Base de datos", command = Bd)
accion1.grid(column=1,row=4)
accion1.configure(state='disabled')
ventana.mainloop()