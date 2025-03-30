El proyecto está orientado a la solucion de un problema real.

Fue solicitado por un negocio de la localidad, con la intencion de manejar de que el sistema manejara el sistema de forma autonoma.

Planteamiento --> Se solicitó un programa que a traves de un codigo de barras permitiera optimizar y agilizar la gestion de inventario en el Local, se solicitó que calcara la estructura de datos(tabla) ya existente -->
  Todo con el fin de que las matematicas y anotaciones repetitivas fueran llevadas por el sistema, dejando al usuario con la unica tarea de calcar los registros ya calculados

Metodología usada --> Se aplicaron algunos fundamentos de la metodología agil, entre ellos estuvo la retroalimentacion constante por parte del cliente, asi como una toma "efectiva"(dentro de lo posible) de requerimientos

Librerias --> Se utilizaron diversas librerias de python, asi como un entorno virtual para asegurar la "perpetuidad" del proyecto;Esto porque python tiene la fama de que sus librerias son muy poco "longevas"
  Entre las librerias se encuentran ->
      --OpenCV(Y Añadidos como NumPY) -- Pillow(Para el manejo de la visualizacion por camara a traves de TKinter ->Actualizacion indefinida de un Label) 
      --PySound(Confirmacion auditiva) --PyZbar(Interpretacion/Decodificacion de los codigos de barra) 
      -- PyBarcode(Creacion de codigo de barra de forma "libre") --SQLite(Integrada con Python) -> Se uso para manejar la base de datos en un archivo
      --Tkinter -> Interfaz grafica -- // CTK->CustomTkinter --> Esta libreria fue la seleccionada para empezar el desarrollo, pero en medio del mismo se optó por regresar a tkinter ( El archivo se mantiene dentro de la estructura de carpetas)

Base de datos -> Se utilizó SQLite para la persistencia de los datos

Este fue mi primer proyecto orientado a una problematica real- Proyecto en 'solitario'
