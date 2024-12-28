import sqlite3
from random import randint,choice
from string import ascii_letters
import os
import barcode as brc

class API():
  def __init__(self,nombre_db):
    self.nombre_db = nombre_db
    conexion = sqlite3.connect(nombre_db + ".db",timeout=2)  # crea la conexión con la base de datos o la crea si no existe
    self.conexion =conexion
    self.cursor = conexion.cursor()


  def crear_tabla(self,nombre_tabla):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    print(nombre_tabla)
    try:
      self.cursor.execute(f"""CREATE TABLE IF NOT EXISTS {nombre_tabla} (
                                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                                    codigo_barras TEXT NOT NULL,
                                    producto TEXT NOT NULL,
                                    precio INT NOT NULL,
                                    existe INTEGER ,
                                    entra INTEGER,
                                    total INTEGER,
                                    queda INTEGER,
                                    ventas INTEGER,
                                    valor INTEGER)"""
                                    )
      self.conexion.commit()
      
    except Exception as e:
       print ("Err: ",e)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None


  def generar_barcode(self, producto):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    self.cursor.execute("SELECT codigo_barras FROM Inventario")
    historico_codigo_barras = self.cursor.fetchall()
    #Elegimos el tipo de codigo de barras a crear
    codigo_barras_ = brc.get_barcode_class('code128')
    #Generamos un valor aleatorio para el barcode
    valor = randint(100, 999)
    #inicializamos la variable codigo_barras
    codigo_barras= None
    '''el while nos asegura que = mientras el #aleatorio ya esté presente en la base de datos
    seguirá generando un codigo hasta que no esté repetido; la condicion se mantiene vigente mientras el
    barcode no esté repetido
    '''
    while True:
      valor = randint(100, 999)
      #convertimos el numero aleatorio a una cadena para concatenarlo con letras al azar
      codigo_barras= str(valor)
      #seleccionamos una posicion de caracter aleatoria
      posicion_random= randint(0, len(codigo_barras))
      #Elegimos una letra random dentro de la libreria String
      letra_random = choice(ascii_letters)
      #Agregamos la letra aleatoria al codigo de barras en una posicion aleatoria, devuelve el string final
      codigo_barras_final = codigo_barras[:posicion_random] + letra_random + codigo_barras[posicion_random:]
      if codigo_barras_final not in historico_codigo_barras and codigo_barras_final != None:
        barcode = codigo_barras_(codigo_barras_final, writer=brc.writer.ImageWriter())
        path_app = os.path.abspath(__file__)
        path_app = os.path.dirname(path_app) # Obtener el directorio del archivo actual path_app = os.path.join(path_app, "barcodes_product") 
        path_app = os.path.join(path_app,"barcodes_product")
        os.makedirs(path_app, exist_ok=True) # Crear la carpeta si no existe
        print(path_app)
        barcode.save(os.path.join(path_app,f"codigo_{codigo_barras_final}_{producto}"))
        break
    return codigo_barras_final





  def agregar_producto(self, producto, existe, precio, entra=0,queda = 0, ventas=0,total = 0):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    #almacena el codigo de barras STRING ya filtrado (irrepetible, 1 letra)
    codigo_barras_final=self.generar_barcode(producto)

    try:
      self.cursor.execute("INSERT INTO inventario(codigo_barras, producto, precio, existe, entra, total, queda, ventas, valor) VALUES (?, ?, ?, ?, ?, ? ,?, ?, ?)", (codigo_barras_final, producto, precio, existe, entra, total,queda, ventas, total,))
      self.conexion.commit()
    except Exception as e:
      print ("Err: agg producto",e)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None

  def mostrar_inventario(self):
    try:
      if not self.conexion:
        self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
        self.cursor = self.conexion.cursor()
      consulta = "SELECT * FROM Inventario"
      self.cursor.execute(consulta)
      return self.cursor.fetchall()
    except Exception as e:
      print ("Err: mostrar inv",e)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None

  def buscar_producto_fetchone(self,codigo_barras):
    self.codigo_barras = codigo_barras
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+"db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      self.cursor.execute("SELECT * FROM Inventario WHERE codigo_barras = ?" ,(self.codigo_barras))
      producto_buscado=self.cursor.fetchone()
      return producto_buscado
    except Exception as e:
      print ("Error: buscar_prod",e)
        
      
  def descontar_producto(self,codigo_barras):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:  
      self.codigo_barras = codigo_barras
      #retorna una lista con los valores del producto escaneado
      producto_scan = self.cursor.buscar_producto_fetchone(self.codigo_barras)
      if producto_scan != None:
          barra_producto = producto_scan[1]
          if producto_scan[3] >=1:
              nueva_cantidad_producto = producto_scan[7]-1
          else:
              pass
          sql= f"UPDTAE Inventario SET ventas = {nueva_cantidad_producto} WHERE codigo_barras = {barra_producto}"
          self.cursor.execute(sql)
          self.conexion.commit()
    except Exception as e:
        print("Error: descontar_prod",e)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None
    
  def eliminar_producto(self, id):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      sql = "DELETE FROM Inventario WHERE id = ?"
      self.cursor.execute(sql, (id,))
      self.conexion.commit()
      print("eliminado")
    except sqlite3.Error as err:
      print("Error: eliminar prod",err)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None

  def modificar_producto(self, id,producto, precio, existe = 0,entra =0,queda = 0, ventas =0):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      sql = "UPDATE Inventario SET producto = ?, precio = ?, existe = ?, entra = ?,queda =?,ventas =? WHERE id = ?"
      self.cursor.execute(sql, (producto, precio, existe,entra,queda ,ventas, id,))
      self.conexion.commit()
      print("Producto modificado")
    except sqlite3.Error as err:
      print("Error: mod prod",err)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None

  def descuento_por_barcode(self,barcode):
    producto_escaneado = self.buscar_por_barcode(barcode)
    # inventario = self.mostrar_inventario()
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      # for registro in inventario:
      #   if registro not in inventario:
      #     return False
      if producto_escaneado is None:
        return False
      print(producto_escaneado)
      if producto_escaneado[7] >=1 :
          nueva_cantidad_ventas = (producto_escaneado[8]) + 1
          #cantidad de producto POST-Venta
          sql = "UPDATE Inventario SET ventas =?  WHERE codigo_barras = ?"         
          self.cursor.execute(sql,(nueva_cantidad_ventas, barcode))
          self.conexion.commit()
          return True
      else:
        print("Producto agotado") 
        return
    except sqlite3.Error as err:
      print("Error: descuento x barcode",err)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None
    
  def buscar_por_barcode(self,barcode):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      sql = "SELECT * FROM Inventario WHERE codigo_barras = ?"
      self.cursor.execute(sql, (barcode,))
      prod=self.cursor.fetchone()
      return prod
    except sqlite3.Error as err:
      print("Error: buscar x barcode",err)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None
  
  def establecer_valores_dinamicos(self):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      sql = "UPDATE Inventario SET total = (existe + entra)"
      self.cursor.execute(sql)
      self.conexion.commit()
      sql = "UPDATE Inventario SET queda = (total - ventas)"
      self.cursor.execute(sql)
      self.conexion.commit()
      sql = "UPDATE Inventario SET valor = (ventas * precio)"
      self.cursor.execute(sql)
      self.conexion.commit()
    except sqlite3.Error as err:
      print("Error: establecer valores dinámicos",err)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None

  def resetear_valores_a_null(self):
    if not self.conexion:
      self.conexion = sqlite3.connect(self.nombre_db+".db",timeout=2)
      self.cursor = self.conexion.cursor()
    try:
      sql = "UPDATE Inventario SET existe = queda, entra = 0, ventas = 0"
      self.cursor.execute(sql)
      self.conexion.commit()
    except sqlite3.Error as err:
      print("Error: resetear valores a NULL",err)
    finally:
      if self.conexion:
        self.conexion.close()
        self.conexion = None
