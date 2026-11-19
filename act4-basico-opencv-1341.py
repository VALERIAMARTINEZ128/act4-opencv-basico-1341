# 0. IMPORTACIÓN DE LIBRERÍAS Y FUNCIONES
# ==============================================================================
import os
import cv2
import numpy as np
import sys
import struct
import win32gui
import win32con
import win32api

# Obtiene la ruta exacta de la carpeta donde está este archivo .py
carpeta_actual = os.path.dirname(os.path.abspath(__file__))

print(' +-+-++-+-Valeria Yaretzi NC 1341+-+-++-+-+')

# 1. LECTURA DE LA IMAGEN DESDE LA CARPETA (SIMULANDO ARCHIVO NO ENCONTRADO)
# ==============================================================================
print("\n1. LECTURA DE IMÁGENES")
nombre_archivo = 'imagen_no_existe.jpeg'  # Nombre intencionalmente incorrecto para probar el error
ruta_pibble = os.path.join(carpeta_actual, nombre_archivo)
img_pibble = cv2.imread(ruta_pibble)

if img_pibble is None:
    mensaje_error = f"Error: No se pudo cargar la imagen '{nombre_archivo}'. Revisa el nombre y ubicación."
    print(mensaje_error)
    
    # Muestra ventana de error nativa de Windows usando win32api
    win32api.MessageBox(
        0,
        mensaje_error,
        "Error de Carga - Valeria Yaretzi 1341",
        win32con.MB_OK | win32con.MB_ICONERROR
    )
    sys.exit()  # Detiene el programa de forma segura
else:
    print("Imagen cargada exitosamente.")