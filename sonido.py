# import numpy as np
from numpy import linspace , pi , sin   
# import sounddevice as sd 
from sounddevice import play, wait
def crear_sonido_caja_registradora():
    # Parámetros del sonido 
    duration = 0.5 
    # Duración en segundos 
    frequency = 1000 
    # Frecuencia en Hertz (ajusta para lograr el sonido deseado) 
    sample_rate = 44100 
    # Tasa de muestreo 
    # # Crear el array de tiempo
    t = linspace(0, duration, int(sample_rate * duration), endpoint=False) 
    # Generar el sonido
    sonido = 0.5 * sin(2 * pi * frequency * t) # Senoide simple 
    # Reproducir el sonido 
    play(sonido, sample_rate) 
    wait()