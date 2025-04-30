import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
# from pyzbar.pyzbar import decode
from zxing import BarCodeReader
import db as con
from time import sleep
from copy import deepcopy
import cv2


import tkinter.messagebox as msb
from tkinter.simpledialog import askinteger
import sonido

class Plantilla_label(tk.Label):
    def __init__(self,aparicion, texto):
        super().__init__(aparicion)
        self.config( font=("Arial", 10,), bg="white", text=texto)

class Plantilla_entry(tk.Entry):
    def __init__(self,aparicion, placeholder_text):
        self.placeholder_text = placeholder_text
        super().__init__(aparicion)
        self.config(width=30, font=("Arial", 15,), relief=tk.RAISED, bg="white")
    

class Plantilla_boton(tk.Button):
    def __init__(self,aparicion,texto_boton):
        super().__init__(aparicion)
        self.config(width=14, height=1, font=("Arial", 9,), relief=tk.RAISED,bg="black",text=texto_boton,fg="white")
        

class Plantilla_ventana(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.conexion = con.API("CRUD")
        self.title("")
        self.geometry("600x400")
        self.config(bg="orange")
        
    

class Ventana_principal(tk.Tk):
    def __init__(self,camara):
        #el parametro <padre> esta ahí para permitirnos ejecutar
        super().__init__()
        self.ventana_inventario = None
        self.ventana_ventas = None
    
        self.camara = camara
        self.cursor = con.API("CRUD")
        self.cursor.crear_tabla("Inventario")
        self.title("Gestión Ventas")
        self.geometry("200x180")
        self.resizable(0,0)
        self.boton_inventario = Plantilla_boton(self,"Asignar_inventario")
        self.boton_inventario.config(command=lambda: self.crear_ventana_inventario())
        self.boton_inventario.pack(anchor=tk.CENTER,padx=15,pady=5)
       
        self.boton_ventas = Plantilla_boton(self,"Empezar Ventas")
        self.boton_ventas.config(command=lambda: self.crear_ventana_ventas() )
        self.boton_ventas.pack(anchor=tk.CENTER,padx=15,pady=5)

        self.var_ventas_grandes = tk.BooleanVar(self)
        boton_ventas_grandes = tk.Checkbutton(self,text="Ventas grandes",font=("arial",8), variable=self.var_ventas_grandes)
        boton_ventas_grandes.pack(pady=8,padx=15,anchor=tk.CENTER)

    def crear_ventana_inventario(self):
        if not self.ventana_inventario or not self.ventana_inventario.winfo_exist():
            self.ventana_inventario =  Ventana_inventario(self.cursor,self)
        else:
            self.ventana_inventario.lift()

    def crear_ventana_ventas(self):
        if not self.ventana_ventas or not self.ventana_ventas.winfo_exist():
            self.ventana_ventas = Ventana_ventas(self.camara,self.cursor,self.var_ventas_grandes,self)
        else:
            self.ventana_ventas.lift()
       


class Ventana_inventario(Plantilla_ventana):
    def __init__(self,cursor,padre):
        super().__init__()
        self.cursor = cursor
        #configuraciones basicas de la pestaña
        self.title("Inventario")
        self.geometry("1200x1100")
        self.resizable(1,1)


        #Creamos el Cuadro donde se mostrará el treeview
        self.frame_inventario = tk.LabelFrame(self, borderwidth=2, border=1)
        self.frame_inventario.grid(columnspan=5, column=0,row=0)


        #Creamos el treeview e inicializamos sus valores de columnas 
        self.tv = ttk.Treeview(self.frame_inventario,columns=("id","codigo_barras","producto","precio","existe","entra","total","queda","ventas","valor"))
        #creamos un conjunto de datos que almacena los valores de c/columna
        # cols = ["id","barcode","producto","cantidad","precio"]
        cols = ["id","codigo_barras","producto","precio","existe","entra","total","queda","ventas","valor"]
        self.tv.column("#0",width=0, stretch=tk.NO)
        #iteramos sobre el conjunto de datos
        for columna in cols:
            #condicionamos la columna ID para hacerla mas pequeña que los demás
            if columna == cols[0]:
                self.tv.column(columna, width=40, anchor=tk.CENTER)
                self.tv.heading(columna,text=columna.capitalize())
            #cuando no es cols[0]<id> = el recuadro del producto sea mas grande
            self.tv.column(columna, width=100, anchor=tk.CENTER)
            self.tv.heading(columna,text=columna.capitalize())
        #empaquetamos el treeview en la pestaña
        self.tv.pack(fill = tk.BOTH, expand=True)
        #mostramos los productos en el treeview
        inv =self.cursor.mostrar_inventario()
        for producto in inv:
            if producto == None:
                self.tv.insert("","end",values="VACIÓ")
            self.tv.insert("", "end", values=producto)
        
        boton_reiniciar_dia = tk.Button(self.frame_inventario,text="¡¡Reiniciar Dia!!",command=lambda:self.reiniciar_dia()  )
        boton_reiniciar_dia.pack(pady=5,padx=5)
        
        ################################################################
        #Creamos Los cuadros donde se mostrarán los diversos widgest
        #creamos el cuadro de los entrys
        self.frame_entrys = tk.LabelFrame(self, text= "Valores de Producto")
        self.frame_entrys.grid(row=1,column=0,padx=15, pady=15)
        
        #creamos el cuadro de los botones
        self.frame_botones = tk.LabelFrame(self,text="Funciones",height=3)
        self.frame_botones.grid(row=2,column=0,pady=15,padx=15,rowspan=5)
        #################################################################

        #Agregamos los entrys de los valores

        self.label_id = Plantilla_label(self.frame_entrys, "ID")
        self.label_id.grid(row=0, column=0, padx=5, pady=5)

        self.entry_id = Plantilla_entry(self.frame_entrys, "ID")
        # self.entry_id.config(state="readonly")
        self.entry_id.grid(row=1, column=0, padx=5, pady=5)

          
        self.label_barcode = Plantilla_label(self.frame_entrys, "Barcode")
        self.label_barcode.grid(row=0, column=1, padx=5, pady=5)

        self.entry_barcode = Plantilla_entry(self.frame_entrys, "Barcode")
        # self.entry_barcode.config(state="readonly")
        self.entry_barcode.grid(row=1, column=1, padx=5, pady=5)



        self.label_producto = Plantilla_label(self.frame_entrys, "Producto*")
        self.label_producto.grid(row=0, column=2, padx=5,pady=5)

        self.entry_producto = Plantilla_entry(self.frame_entrys, "Producto*")
        self.entry_producto.grid(row=1, column=2, padx=5, pady=5)


        self.label_precio = Plantilla_label(self.frame_entrys, "Precio*")
        self.label_precio.grid(row=2, column=0, padx=5, pady=5)

        self.entry_precio = Plantilla_entry(self.frame_entrys, "Precio*")
        self.entry_precio.grid(row=3, column=0, padx=5, pady=5)



        self.label_existe = Plantilla_label(self.frame_entrys, "Existe*")
        self.label_existe.grid(row=2, column=1, padx=5, pady=5)
        self.entry_existe = Plantilla_entry(self.frame_entrys, "Existe*")
        self.entry_existe.grid(row=3, column=1, padx=5, pady=5)

        self.label_entra = Plantilla_label(self.frame_entrys, "Entra")
        self.label_entra.grid(row=2, column=2, padx=5)
        self.entry_entra = Plantilla_entry(self.frame_entrys, "Entra")
        self.entry_entra.grid(row=3, column=2, padx=5)


        self.label_ventas = Plantilla_label(self.frame_entrys, "Ventas")
        self.label_ventas.grid(row=4, column=1, padx=5)
        self.entry_ventas = Plantilla_entry(self.frame_entrys, "Ventas")
        self.entry_ventas.grid(row=5, column=1, padx=5)


        #creamos un boton para limpiar los entrys

        self.boton_limpiar = Plantilla_boton(self.frame_entrys,"Limpiar Valores")
        self.boton_limpiar.config(command=self.limpiar_entrys,width=50,height=2)
        self.boton_limpiar.grid(row=5,column=2,padx=7,pady=10)


        #Agregamos botones 
        self.boton_añadir_producto = Plantilla_boton(self.frame_botones,"Añadir producto")
        self.boton_añadir_producto.config(width=30,height=2,command=lambda: self.añadir_producto(self.cursor))
        self.boton_añadir_producto.grid(row=0,column=1,pady=10,padx=7)

        self.boton_modificar_producto = Plantilla_boton(self.frame_botones,"Modificar Producto")
        self.boton_modificar_producto.config(width=30,height=2,command=lambda : self.modificar_producto(self.cursor))
        self.boton_modificar_producto.grid(row=0,column=2,padx=7,pady=10)

        self.boton_eliminar_producto = Plantilla_boton(self.frame_botones,"Eliminar Producto")
        self.boton_eliminar_producto.config(width=30,height=2,command=lambda: self.eliminar_producto(self.cursor))
        self.boton_eliminar_producto.grid(row=0,column=3,padx=7,pady=10)

        self.boton_actualizar_tabla= Plantilla_boton(self.frame_botones,"Actualizar Inventario")
        self.boton_actualizar_tabla.config(command=self.actualizar_tv,width=30,height=2)
        self.boton_actualizar_tabla.grid(row=0,column=4)

        self.actualizar_tv()

        self.tv.bind("<ButtonRelease-1>", self.seleccionar_registro)

    def reiniciar_dia(self):
        if msb.askyesno("!!!!!!!!!","ESTA ACCION NO SE PUEDE DESHACER. PROSEGUIR IMPLICA ELIMINAR TODOS LOS REGISTROS ALMACENADOS HASTA AHORA, SIN POSIBILIDAD DE RECUPERACION"):
            self.cursor.resetear_valores_a_null()
            self.actualizar_tv()

        else:
            return

    def limpiar_entrys(self):
        self.entry_id.delete(0, tk.END)
        self.entry_producto.delete(0, tk.END)
        self.entry_barcode.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)
        self.entry_existe.delete(0,tk.END)
        self.entry_entra.delete(0, tk.END)
        self.entry_ventas.delete(0, tk.END)
    
    def rellenar_valores_automaticos(self):
        self.cursor.establecer_valores_dinamicos()

        

    def actualizar_tv(self):
        self.rellenar_valores_automaticos()
        #insertamos datos actualziados
        self.tv.delete(*self.tv.get_children())  # Elimina todos los elementos actuales
        inventario = self.cursor.mostrar_inventario()
        for producto in inventario:
            self.tv.insert("", "end", values=producto)
    def seleccionar_registro(self,event):
        self.limpiar_entrys()
        selected = self.tv.focus()
        values = self.tv.item(selected, 'values')
        print("valores ===",values)

        if len(selected) >= 1:
           #Devuelve todos los datos del item seleccionado/
            self.entry_id.insert(0,values[0])
            self.entry_barcode.insert(0,values[1])
            self.entry_producto.insert(0,values[2])
            self.entry_precio.insert(0,values[3])
            self.entry_existe.insert(0,values[4])
            self.entry_entra.insert(0,values[5])
            self.entry_ventas.insert(0,values[8])
            
        else:
            tk.messagebox.showinfo("Error", "No has seleccionado ningún producto.")

    def añadir_producto(self,cursor):
        self.cursor = cursor
       
        producto = self.entry_producto.get()
        existe = self.entry_existe.get()
        precio = self.entry_precio.get()
        if  producto == "" or existe == "" or precio == "":
            msb.showerror("!!","Campos vacíos")
            return
        inventario= self.cursor.mostrar_inventario()
        for item in inventario:
            if  item[1] ==producto:
                msb.showerror("Error"," Producto ya existente")
                return
        self.cursor.agregar_producto(producto, existe, precio)
        self.actualizar_tv()
    
    def eliminar_producto(self, cursor):
        self.cursor = cursor
        id = self.entry_id.get()
        self.cursor.eliminar_producto(id)
        self.actualizar_tv()
    
    def modificar_producto(self,cursor):
        self.cursor = cursor
        id = self.entry_id.get()
        producto = self.entry_producto.get()
        existe = self.entry_existe.get()
        entra = self.entry_entra.get()
        precio = self.entry_precio.get()
        ventas = self.entry_ventas.get()

        if  producto == "" or existe == "" or precio == "":
            msb.showerror("!!","Campos vacíos")
            return
        self.cursor.modificar_producto(id, producto,precio, existe,entra,ventas=ventas)
        self.actualizar_tv()


    


class Ventana_ventas(Plantilla_ventana):
    def __init__(self,camara,cursor,control_ventas,padre):
        self.var_ventas_grandes= control_ventas
        self.padre  = padre
        super().__init__()
        self.cursor = cursor
        self.camara = camara
        self.title("Ventas")
        self.geometry("800x800")
        self.resizable(1,1)


        self.frame_ventas = tk.LabelFrame(self, borderwidth=2, border=1,text="Lector Codigo")
        self.frame_ventas.pack(fill="both", expand=True) 
        
        self.label_cam = tk.Label(self.frame_ventas) 
        self.label_cam.pack() 

        # self.var_ventas_grandes = tk.BooleanVar(self.frame_ventas)
        # self.boton_ventas_grandes = tk.Checkbutton(self.frame_ventas,text="Ventas grandes",font=("arial",8), variable=self.var_ventas_grandes)
        # self.boton_ventas_grandes.pack(pady=8,padx=15,anchor=tk.CENTER)

        self.label_ultima_venta = tk.Label(self.frame_ventas,font=("Arial", 20,))
        self.label_ultima_venta.pack(pady=30)
        self.image= None     
       


        self.comprobacion = {} 
        
        self.update_frame()
    
    def update_frame(self):
        #Lector de codigo de barras del zxing
        reader = BarCodeReader()

        var_ventas_grandes=self.var_ventas_grandes.get()
    
        frame = self.camara.get_frame() 
        barcodes = reader.decode(frame)
        if frame is not None: 
            for barcode in barcodes:
                (x,y,w,h)= barcode.rect
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                barcode_value= barcode.data.decode("utf-8")
                if barcode_value != None:
                    cv2.putText(frame,barcode_value,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
                    print(barcode_value)
                    print(self.comprobacion)
                    value = self.comprobacion.get(barcode_value)
                    if value is not None and value >=15:
                        print("barcode leido correctamente")
                        comprobacion_temp = deepcopy(self.comprobacion)
                        producto_sel= self.conexion.buscar_por_barcode(barcode_value)

                        if var_ventas_grandes != False and producto_sel != None:
                            cantidad_venta= askinteger("Venta Grande","Ingrese una cantidad de elemntos ",minvalue=1,initialvalue=1)   
                            if cantidad_venta ==1:
                                self.cursor.descuento_por_barcode(barcode_value)
                            
                            for i in range (1,cantidad_venta):
                                self.conexion.descuento_por_barcode(barcode_value)
                                

                        if var_ventas_grandes == None:
                            self.label_ultima_venta.config(text="Error al seleccionar cantidad de productos")
                            return
                        else:
                            #ret almacena true o false, según si el producto existe en la base de datos o no 
                            ret = self.cursor.descuento_por_barcode(barcode_value)
                            if ret:
                                ultimo_producto = self.cursor.buscar_por_barcode(barcode_value)
                                self.label_ultima_venta.config(text=f"Ultimo producto vendido fue = {ultimo_producto[2]}")
                            elif not ret:
                                self.label_ultima_venta.config(text="Producto no Encontrado")
                        
                        for clave in comprobacion_temp: 
                            del self.comprobacion[clave]
                            print(f"El código {clave} se eliminó de falsos positivos")
                        sonido.crear_sonido_caja_registradora()
                        if self.padre.ventana_inventario:
                            self.padre.ventana_inventario.actualizar_tv()
                        sleep(1.5)
                    if barcode_value not in self.comprobacion:
                        self.comprobacion[barcode_value] = 1
                    if barcode_value in self.comprobacion:
                        self.comprobacion[barcode_value]+=1
            image = Image.fromarray(frame)   
            self.image = ImageTk.PhotoImage(image)
            self.label_cam.configure(image=self.image)
            self.label_cam.image = self.image
        self.after(10, self.update_frame)


         
            
    def on_closing(self):
        self.camara.release()
        self.destroy()

        

        

        



    