## Autor: Luis Fernando Morales Mejicanos
## 201020573
## Octubre de 2014

#!/usr/bin/python

from gi.repository import Gtk, GObject, Gdk, GLib
from random import randrange
import math
import os

class Principal(Gtk.Window):
    
    def __init__(self):
        Gtk.Window.__init__(self,title="Gradiente descendente")
        
        tabla = Gtk.Table(5,3,True)
        self.add(tabla)
        
        tabla.set_row_spacing(0,5)
        tabla.set_col_spacing(0,10)
        
        label = Gtk.Label("Archivo de X")
        label1 = Gtk.Label("Archivo de Y")
        label3 = Gtk.Label("Alpha")
        label4 = Gtk.Label("Tolerancia")
        label5 = Gtk.Label("Iteraciones")
        
        self.campoArchivoX=Gtk.Entry()
        self.campoArchivoY=Gtk.Entry()
        self.campoAlpha = Gtk.Entry()
        self.campoTol = Gtk.Entry()
        self.campoIteraciones = Gtk.Entry()
        self.botonAnalizar = Gtk.Button(label="Analizar")
        self.botonGetX = Gtk.Button(label="...")
        self.botonY = Gtk.Button(label="...")
        
        tabla.attach(label,0,1,1,3)
        tabla.attach(self.campoArchivoX,1,3,1,3)
        tabla.attach(self.botonGetX,3,4,1,3)
        tabla.attach(label1,0,1,3,5)
        tabla.attach(self.campoArchivoY,1,3,3,5)
        tabla.attach(self.botonY,3,4,3,5)
        tabla.attach(label3,0,1,5,7)
        tabla.attach(self.campoAlpha,1,3,5,7)
        tabla.attach(label4,0,1,7,9)
        tabla.attach(self.campoTol,1,3,7,9)
        tabla.attach(label5,0,1,9,11)
        tabla.attach(self.campoIteraciones,1,3,9,11)
        tabla.attach(self.botonAnalizar,3,4,11,13)

        self.botonGetX.connect("clicked",self.botonX_onClick)
        self.botonY.connect("clicked",self.botonY_onClick)
        self.botonAnalizar.connect("clicked",self.analizar_onClick)
        
    def botonX_onClick(self,widget):
        chooser = Gtk.FileChooserDialog("Seleccionar un archivo",self,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(chooser)
        response = chooser.run()
        
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + chooser.get_filename())
            self.campoArchivoX.set_text(chooser.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
            
        chooser.destroy()
        
    def botonY_onClick(self,widget):
        chooser = Gtk.FileChooserDialog("Seleccionar un archivo",self,
                                        Gtk.FileChooserAction.OPEN,
                                        (Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
                                         Gtk.STOCK_OPEN, Gtk.ResponseType.OK))
        self.add_filters(chooser)
        response = chooser.run()
        
        if response == Gtk.ResponseType.OK:
            print("Open clicked")
            print("File selected: " + chooser.get_filename())
            self.campoArchivoY.set_text(chooser.get_filename())
        elif response == Gtk.ResponseType.CANCEL:
            print("Cancel clicked")
        chooser.destroy()
        
    def add_filters(self, dialog):
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/csv")
        dialog.add_filter(filter_text)

        filter_any = Gtk.FileFilter()
        filter_any.set_name("Any files")
        filter_any.add_pattern("*")
        dialog.add_filter(filter_any)
        
    def analizar_onClick(self,widget):
        if self.campoArchivoX.get_text() is None:
            return
        
        if self.campoArchivoY.get_text() is None:
            return
        
        if self.campoAlpha.get_text() is None:
            return

        if self.campoTol.get_text() is None:
            return
        
        if self.campoIteraciones.get_text() is None:
            return
        
        archivoX = open(self.campoArchivoX.get_text(),'rU')
        
        archivoY= open(self.campoArchivoY.get_text(),'rU')
        
        if not archivoX is None and not archivoY is None:
            alpha = float(self.campoAlpha.get_text())
            tol = float(self.campoTol.get_text())
            it = float(self.campoIteraciones.get_text())
            
            listaX = []
            for line in archivoX:
                linea = line.strip()
                elementos = linea.split(',')
                for i in range(len(elementos)):
                    elementos[i]=float(elementos[i])
                
                listaX.append(elementos)
                
            #self.escalar(listaX)
            
            listaY = []
            for line in archivoY:
                linea = line.strip()
                elementos = linea.split(',')
                for i in range(len(elementos)):
                    elementos[i]=float(elementos[i])
                
                listaY.append(elementos)
            
            resultado = self.gradiente_desc(listaX,listaY, alpha, tol, it)
            
            if not resultado is None:
                res_path = self.campoArchivoX.get_text()+'.res'
                archivo = open(res_path,'w')
                
                str_res = ""
                for i in range (len(resultado)):
                    str_res += `resultado[i]`
                    if i < len(resultado)-1:
                        str_res+="\r"

                archivo.write(str_res)
            
        else:
            return
        
    
    def get_max(self,listado):
        maximo = 0.0
        tam = len(listado)
        for i in range(tam):
            if i==0:
                maximo = listado[i]
            else:
                if listado[i]>maximo:
                    maximo = listado[i]
        
        return maximo
    
    def escalar(self,listaX):
        n = len(listaX[0])
        m = len(listaX)
        for j in range(n):
            listado = []
            for i in range(m):
                listado.append(listaX[i][j])
            
            maximo = self.get_max(listado)
            
            for i in range(m):
                listaX[i][j] = listaX[i][j]/maximo
            
    
    def actualizarCosto(self,thetas,costos,m,n,x,y):
            for i in range(m):
                costo_n=0
                for j in range(n):
                    costo_n=costo_n+thetas[j]*x[i][j]
                costo_n = costo_n - y[i][0]
                costos.append(costo_n)
                
    def gradiente_desc(self,x,y,alfa,tolerancia,iteraciones):
        it = 0
        m = len(x)
        if m!=len(y) :
            return
        n = len(x[0])
        theta = []
        for i in range(n):
            theta.append(randrange(0,1))
        
        costos_i = []
        
        while it<iteraciones:
            costos=[]
            theta_antigua = []
            for i in range(len(theta)):
                theta_antigua.append(theta[i])
                
            self.actualizarCosto(theta, costos, m, n, x, y)
            
            for j in range(n):
                theta_temp=0
                
                for i in range(m):
                    theta_temp = theta_temp +costos[i]*x[i][j]
        
                theta[j]=theta[j]-(alfa/m)*theta_temp
                
                self.actualizarCosto(theta, costos, m, n, x, y)
            
            c = 0.0
            for i in range(len(costos)):
                c=c + (costos[i]*costos[i])
                
            c = (1.0/(2.0*m))*c
            
            costos_i.append(0.0)
            costos_i[it]=c
                
            sale = False
            
            if it>0:
                sale = math.fabs(costos_i[it]-costos_i[it-1])<= tolerancia
                #sale = costos_i[it]<=tolerancia
                
            if sale:
                break
            it=it+1
        
        str_theta = ""
        
        for i in range (len(theta)):
            str_theta+="theta"+`i`+"="
            str_theta+=`theta[i]`
            if i < len(theta)-1:
                str_theta+=','
        print str_theta
            
        return costos_i
            
win = Principal()

win.connect("delete-event",Gtk.main_quit)
win.show_all()
Gtk.main()