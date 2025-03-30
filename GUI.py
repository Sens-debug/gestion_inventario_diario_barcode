#HOJA DE CODIGO NO UTILIZADA

import tkinter as tk
from tkinter import ttk
import customtkinter as Ctk #ctk customTkinter
import db as con



class Ventana_principal(Ctk.CTk):
    def __init__(self):
        super().__init__()  # Hereda de la clase tk.Tk()
        self.camara= camara
        self.cursor = con.API("CRUD")
        self.title("Sistema Gestión Ventas")
        self.dark_mode = Ctk.set_appearance_mode("dark")
        self.button_config = Ctk.set_default_color_theme("blue")
        self.resizable(0,0)
        self.geometry("300x300")
        self.attributes("-topmost",True) # focus
        self.crear_widget_principal()

    def update_frame(self,frame_objetivo):
        
        # self.update_idletasks()
        # self.label_bienvenido.configure(text=f"BIENVENIDO AL SISTEMA - {self.camara.get_frame()}")
        # self.after(1000, self.update_frame) # Actualiza la ventana cada segundo
        # self.label_bienvenido.pack()

        def update_frame(self): 
            frame = self.camera.get_frame() 
            if frame is not None:
                image = Ctk.CTkImage.fromarray(frame)
                
                self.label.configure(image=image) 
                self.label.image = image 
                self.root.after(10, self.update_frame)

    def crear_widget_principal(self):
        frame_principal = Ctk.CTkFrame(self,fg_color=None)
        frame_principal.pack()
        self.label_bienvenido = Ctk.CTkLabel(frame_principal,text="BIENVENIDO AL SISTEMA")
        self.label_bienvenido.grid(column=0, row=0, pady=20,padx=20)
        buttons = Ctk.CTkButton(frame_principal, text="EMPEZAR VENTAS",command=lambda :self.crear_ventana_ventas())
        buttons.grid(column=0, row=1, pady=20)
        buttons = Ctk.CTkButton(frame_principal, text="ASIGNAR INVENTARIO", command= lambda: self.crear_ventana_inventario())
        buttons.grid(column=0, row=2, pady=20)

    def crear_ventana_ventas(self):
        self.ventana_ventas = Ctk.CTkToplevel()
        self.ventana_ventas.geometry("1000x1200")
        self.ventana_ventas.attributes("-topmost",True) # focus
        frame_ventana_ventas = Ctk.CTkFrame(self.ventana_ventas,fg_color=None)
        frame_ventana_ventas.pack()
        self.ventana_ventas.title("VENTAS")

        self.update_frame(frame_objetivo=frame_ventana_ventas)
       

    def crear_ventana_inventario(self):
        self.ventana_inventario = Ctk.CTkToplevel()
        self.ventana_inventario.geometry("1000x1200")
        self.ventana_inventario.title("INVENTARIO")
        self.ventana_inventario.attributes("-topmost",True) # focus
        self.ventana_inventario.resizable(0,0)
        frame_ventana_inventario = Ctk.CTkFrame(self.ventana_inventario,fg_color=None)
        frame_ventana_inventario.pack()

        self.tabla_tv=ttk.Treeview(frame_ventana_inventario,columns=("id","bar_code","producto","cantidad","precio"))
        cols = ["id","bar_code","producto","cantidad","precio"]
        self.tabla_tv.column("#0",width=0, stretch=tk.NO)
        index = 0
        for col in cols:
            #if controla que el recuadro del ID sea mas pequeño(w=40)
            if col == cols[0]:
                self.tabla_tv.column(col, width=40, anchor= tk.CENTER)
                self.tabla_tv.heading(col,text=col.capitalize())
            #Cuando no es cols[0]<id> = el recuadro del producto sea mas grande(w=200)
            self.tabla_tv.column(col,width=200,anchor=tk.CENTER)
            self.tabla_tv.heading(col,text=col.capitalize())
            index+=1
        self.tabla_tv.pack(fill=tk.BOTH, expand=True)
        inventario = self.cursor.mostrar_inventario()
        for producto in inventario:
            self.tabla_tv.insert("", "end", values=producto)

        self.textvar_mod_producto= Ctk.StringVar()
        
        self.textvar_mod_cantidad= Ctk.IntVar()
        self.textvar_mod_cantidad.set("")
        
        self.textvar_mod_precio= Ctk.IntVar()
        self.textvar_mod_precio.set("")

        Ctk.CTkLabel(frame_ventana_inventario,text="Producto").pack(anchor= "w", pady=1,padx=10)
        self.entry_modificacion_producto = Ctk.CTkEntry(frame_ventana_inventario,placeholder_text="Producto",textvariable=self.textvar_mod_producto)
        self.entry_modificacion_producto.pack(anchor= "w", pady=1,padx=10)

        Ctk.CTkLabel(frame_ventana_inventario,text="Cantidad").pack(anchor= "w", pady=1,padx=10)
        self.entry_modificacion_cantidad = Ctk.CTkEntry(frame_ventana_inventario,placeholder_text="Cantidad",textvariable=self.textvar_mod_cantidad)
        self.entry_modificacion_cantidad.pack(anchor = "w", pady=1,padx=10)

        Ctk.CTkLabel(frame_ventana_inventario,text="Precio").pack(anchor= "w", pady=1,padx=10)
        self.entry_modificacion_precio = Ctk.CTkEntry(frame_ventana_inventario,placeholder_text="Precio",textvariable=self.textvar_mod_precio)
        self.entry_modificacion_precio.pack(anchor = "w", pady=1,padx=10)

        boton_añadir_registro= Ctk.CTkButton(frame_ventana_inventario,text="Añadir producto", command= lambda:self.crear_ventana_añadir_producto_tv())
        boton_añadir_registro.pack()

        boton_eliminar_registro= Ctk.CTkButton(frame_ventana_inventario,text="Eliminar producto", command= lambda:self.eliminar_producto_tv())
        boton_eliminar_registro.pack()

        boton_editar_registro= Ctk.CTkButton(frame_ventana_inventario,text="Editar producto", command= lambda:self.editar_producto_tv())
        boton_editar_registro.pack()

        boton_actualizar_tv = Ctk.CTkButton(frame_ventana_inventario, text=" Refrescar Panel", command= lambda: self.actualizar_tv())
        boton_actualizar_tv.pack()
        
        self.tabla_tv.bind("<<TreeviewSelect>>",self.rellenar_entrys_mod())
    def actualizar_tv(self):
        self.tabla_tv.delete(*self.tabla_tv.get_children())  # Elimina todos los elementos actuales
        inventario = self.cursor.mostrar_inventario()
        for producto in inventario:
            self.tabla_tv.insert("", "end", values=producto)

    def crear_ventana_añadir_producto_tv(self):
        producto_var_control_entry = Ctk.StringVar()
        
        cantidad_var_control_entry = Ctk.IntVar()
        cantidad_var_control_entry.set("")

        precio_var_control_entry = Ctk.IntVar()
        precio_var_control_entry.set("")

        ventana_auxiliar = Ctk.CTkToplevel(self)
        ventana_auxiliar.geometry("400x300")
        ventana_auxiliar.title("Añadir producto")
        ventana_auxiliar.attributes("-topmost",True) # focus
        frame_ventana_auxiliar = Ctk.CTkFrame(ventana_auxiliar,fg_color=None)
        frame_ventana_auxiliar.pack()
        
        Ctk.CTkLabel(frame_ventana_auxiliar,text="Producto :").pack()
        self.entry_producto = Ctk.CTkEntry(frame_ventana_auxiliar,textvariable=producto_var_control_entry)
        self.entry_producto.pack()
        

        Ctk.CTkLabel(frame_ventana_auxiliar,text="Cantidad de producto :").pack()
        self.entry_cantidad = Ctk.CTkEntry(frame_ventana_auxiliar,textvariable=cantidad_var_control_entry)
        self.entry_cantidad.pack()

        Ctk.CTkLabel(frame_ventana_auxiliar,text="Precio del producto :").pack()
        self.entry_precio = Ctk.CTkEntry(frame_ventana_auxiliar,textvariable=precio_var_control_entry)
        self.entry_precio.pack()

        boton_añadir_producto= Ctk.CTkButton(frame_ventana_auxiliar,text="Añadir producto", command= lambda:self.cursor.agregar_producto(producto_var_control_entry.get(),cantidad_var_control_entry.get(),precio_var_control_entry.get()))
        boton_añadir_producto.pack(pady=7)

        boton_limpiar_entrys = Ctk.CTkButton(frame_ventana_auxiliar, text="Limpiar Campos",  command= lambda: self.limpiar_entrys())
        boton_limpiar_entrys.pack(pady=5)

    def limpiar_entrys(self):
        self.actualizar_tv()
        self.entry_producto.delete(0, tk.END)
        self.entry_cantidad.delete(0, tk.END)
        self.entry_precio.delete(0, tk.END)

    def eliminar_producto_tv(self):
        #crea una lista de listas con los seleccionados en el TV, [0] elige la primer lista ==primer seleccionado
        seleccionado = self.tabla_tv.selection()
        
        if len(seleccionado) >= 1:
            seleccionado = seleccionado[0]
            #Devuelve todos los datos del item seleccionado/
            producto_values = self.tabla_tv.item(seleccionado,'values')
            producto_id = producto_values[0]
            self.cursor.eliminar_producto(producto_id)
            self.actualizar_tv()
        else:
            tk.messagebox.showinfo("Error", "No has seleccionado ningún producto.")

    def rellenar_entrys_mod(self):
        self.actualizar_tv()
        #crea una lista de listas con los seleccionados en el TV, [0] elige la primer lista == primer seleccionado
        seleccionado = self.tabla_tv.focus()
        print(seleccionado)
        
        if len(seleccionado) >= 1:
            #Devuelve todos los datos del item seleccionado/
            producto_values = self.tabla_tv.item(seleccionado,'values')
            
            self.entry_modificacion_cantidad.insert(0,producto_values[3])
            self.entry_modificacion_precio.insert(0,producto_values[4])
            self.entry_modificacion_producto.insert(0,producto_values[2])
            self.actualizar_tv()
            
        else:
            tk.messagebox.showinfo("Error", "No has seleccionado ningún producto.")
      

        

