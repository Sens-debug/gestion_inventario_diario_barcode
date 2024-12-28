import barcode.writer
import cv2
from pyzbar.pyzbar import decode
from time import sleep
import barcode
from copy import deepcopy

# Elegimos el tipo de código de barras 'code128'
codigo_barras = barcode.get_barcode_class('code128')

# Crear el código de barras a partir de un valor (puede ser alfanumérico)
valor = "87V6"  # Puede ser cualquier cadena alfanumérica

# Generar el código de barras
codigo = codigo_barras(valor, writer=barcode.writer.ImageWriter())

# Guardar el código de barras como una imagen PNG
codigo.save("codigo_code128")

print("Código de barras generado con éxito.")
camara = cv2.VideoCapture(0)
barcode_value = None
comprobacion = {}
while camara.isOpened():
        ret, frame = camara.read()
        if ret:
            barcodes = decode(frame)
            for barcode in barcodes:
                (x,y,w,h)= barcode.rect
                cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
                barcode_value= barcode.data.decode("utf-8")
                cv2.putText(frame,barcode_value,(x,y-10),cv2.FONT_HERSHEY_SIMPLEX,0.9,(0,255,0),2)
                print(barcode_value)
                print(comprobacion)
                value = comprobacion.get(barcode_value)
                if value is not None and value >=15:
                    print("barcode accedido correctamente")
                    comprobacion_temp = deepcopy(comprobacion)
                    for clave in comprobacion_temp: 
                        val_iterable= comprobacion.get(clave)
                        del comprobacion[clave]
                        print(f"El código {clave} ha sido eliminado del inventario")
                    sleep(2)

                if barcode_value not in comprobacion:
                    comprobacion[barcode_value] = 1

                if barcode_value in comprobacion:
                     comprobacion[barcode_value] +=1
                barcode_value = None
            cv2.imshow("Barcode Scanner",frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
       
camara.release()
cv2.destroyAllWindows()

