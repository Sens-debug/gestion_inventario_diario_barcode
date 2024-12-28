import db as con
import GUI_tk as G
import camara_brcode as c_brcode
'''
@credits
Nm = Juan Miguel Santamaría Múnera
mail = jsantamariamunera@gmail.com
Github = https://github.com/Sens-debug
'''

if __name__ == "__main__":
    try:
        camara = c_brcode.Camara()
    
        app= G.Ventana_principal(camara)     
        app.mainloop()
    finally:
        if app.cursor.conexion:
            app.cursor.conexion.close()
        camara.release_cam()
        