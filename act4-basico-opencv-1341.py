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

def convertir_jpg_a_ico(ruta_jpg, ruta_ico):
    img_ico = cv2.imread(ruta_jpg, cv2.IMREAD_UNCHANGED)
    if img_ico is None:
        return False
    
    img_ico = cv2.resize(img_ico, (32, 32), interpolation=cv2.INTER_AREA)
    
    # Si no tiene canal alfa (transparencia), se lo agregamos (BGRA)
    if img_ico.shape[2] == 3:
        img_ico = cv2.cvtColor(img_ico, cv2.COLOR_BGR2BGRA)
    
    # En formato ICO, los píxeles van invertidos verticalmente
    img_ico = cv2.flip(img_ico, 0)
    
    # Construimos la cabecera binaria estándar de un archivo .ico de 32x32
    ico_header = struct.pack('<HHH', 0, 1, 1)
    bmp_header = struct.pack('<IIIHHIIIIII', 40, 32, 64, 1, 32, 0, 0, 0, 0, 0, 0)
    and_mask = b'\x00' * (32 * 4)
    dib_data = bmp_header + img_ico.tobytes() + and_mask
    dir_entry = struct.pack('<BBBBHHII', 32, 32, 0, 0, 1, 32, len(dib_data), 22)
    
    with open(ruta_ico, 'wb') as f:
        f.write(ico_header + dir_entry + dib_data)
    return True

def cambiar_icono_ventana(nombre_ventana, ruta_icono):
    hwnd = win32gui.FindWindow(None, nombre_ventana)
    if hwnd:
        try:
            hicon = win32gui.LoadImage(
                0, 
                ruta_icono, 
                win32con.IMAGE_ICON, 
                0, 
                0, 
                win32con.LR_LOADFROMFILE | win32con.LR_DEFAULTSIZE
            )
            win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_SMALL, hicon)
            win32api.SendMessage(hwnd, win32con.WM_SETICON, win32con.ICON_BIG, hicon)
        except Exception as e:
            print(f"Advertencia: No se pudo cargar el icono ({e})")

print(' +-+-++-+-Valeria Yaretzi NC 1341+-+-++-+-+')

# 1. LECTURA DE LA IMAGEN DESDE LA CARPETA
# ==============================================================================
print("\n1. LECTURA DE IMÁGENES")
ruta_pibble = os.path.join(carpeta_actual, 'pibble.jpeg')
img_pibble = cv2.imread(ruta_pibble)

if img_pibble is None:
    print("Error: No se pudo leer 'pibble.jpeg'. Revisa el nombre y ubicación.")
    sys.exit()
else:
    print("Imagen de Pibble cargada exitosamente.")

# 2. PROPIEDADES DE LA IMAGEN
# ==============================================================================
print("\n2. PROPIEDADES DE LA IMAGEN 1341")
height, width, channels = img_pibble.shape
print(f"Dimensiones de la imagen: {width}x{height} píxeles")
print(f"Número de canales de color: {channels}")
print(f"Tipo de dato de la imagen: {img_pibble.dtype}")
print(f"Total de datos/píxeles: {img_pibble.size}")

# 3. VISUALIZACIÓN DE LA IMAGEN ORIGINAL
# ==============================================================================
nombre_ventana = 'Gpo 3H Pibble Original Valeria Yaretzi 1341'

# Rutas exactas para tu icono.jpeg y el archivo .ico que se generará
ruta_icono_origen = os.path.join(carpeta_actual, 'icono.jpeg')
ruta_icono_destino = os.path.join(carpeta_actual, 'icono.ico')

# 1ro: Convertimos tu 'icono.jpeg' a 'icono.ico' en esa misma carpeta
convertir_jpg_a_ico(ruta_icono_origen, ruta_icono_destino)

print("\n3. 🐶 MOSTRANDO IMAGEN ORIGINAL de Pibble")
print("Presiona cualquier tecla sobre la ventana de la imagen para continuar...")

cv2.imshow(nombre_ventana, img_pibble)
cambiar_icono_ventana(nombre_ventana, ruta_icono_destino)  # 2do: Aplicamos el .ico recién creado

cv2.waitKey(0)
cv2.destroyAllWindows()

print("-+-+-+-modificando pixeles 1341+-+-+-+-+")
# ==============================================================================
# 4. ACCESO Y MODIFICACIÓN DE PÍXELES INDIVIDUALES
# ==============================================================================
print("\n4. ACCEDIENDO Y MODIFICANDO PÍXELES")  # Imprime el título de la cuarta sección.
pixel_img = img_pibble.copy()  # Crea una copia exacta de la imagen original para no dañar la original.

y, x = 100, 150  # Define las coordenadas a analizar: fila (Y) = 100, columna (X) = 150.
pixel = pixel_img[y, x]  # Obtiene los 3 valores de color [Azul, Verde, Rojo] del píxel en esa posición.
print(f"Valor del píxel en ({x}, {y}): {pixel} (Formato BGR)")  # Imprime los valores BGR del píxel en consola.

pixel_img[y, x] = [0, 0, 255]  # Cambia el color de ese único píxel a Rojo puro (0 Azul, 0 Verde, 255 Rojo).
cv2.circle(pixel_img, (x, y), 15, (0, 255, 255), 2)  # Dibuja un círculo amarillo alrededor para poder verlo a simple vista.

cv2.imshow('Pixel Modificado valeria yaretzi 1341', pixel_img)  # Muestra la imagen con el píxel alterado y señalado.
cv2.waitKey(0)  # Espera a que se presione una tecla para continuar.

# ==============================================================================
# 5. REGIÓN DE INTERÉS (ROI - REGION OF INTEREST)
# ==============================================================================
print("\n5. REGIÓN DE INTERÉS (ROI)")  # Imprime el título de la quinta sección.
roi_img = img_pibble.copy()  # Crea una nueva copia limpia de la imagen original.

roi = roi_img[50:200, 100:300]  # Recorta una sub-matriz desde la fila 50 a 200 y columna 100 a 300.
cv2.rectangle(roi_img, (100, 50), (300, 200), (0, 255, 0), 2)  # Dibuja un rectángulo verde marcando la zona recortada.

cv2.imshow('Imagen con ROI marcada valeria yaretzi 1341', roi_img)  # Muestra la imagen completa con el recuadro verde.
cv2.waitKey(0)  # Espera a que se presione una tecla.

cv2.imshow('ROI Extraida (Recorte) valeria yaretzi 1341', roi)  # Muestra únicamente el pedazo recortado en una ventana aparte.
cv2.waitKey(0)  # Espera a que se presione una tecla.


# 6. SEPARACIÓN Y FUSIÓN DE CANALES DE COLOR (BGR)
# ==============================================================================
print("\n6. SEPARANDO Y FUSIONANDO CANALES")  # Imprime el título de la sexta sección.
b, g, r = cv2.split(img_pibble)  # Divide la imagen a color en 3 matrices independientes: Azul (b), Verde (g) y Rojo (r).

cv2.imshow('Canal Azul (Escala de grises)', b)  # Muestra la intensidad del canal azul en tonos de gris.
cv2.imshow('Canal Verde (Escala de grises)', g)  # Muestra la intensidad del canal verde en tonos de gris.
cv2.imshow('Canal Rojo (Escala de grises)', r)  # Muestra la intensidad del canal rojo en tonos de gris.
cv2.waitKey(0)  # Pausa el programa mientras observas las 3 ventanas en blanco y negro.

zeros = np.zeros_like(b)  # Crea una matriz llena de ceros (negro) del mismo tamaño que un canal.
blue_img = cv2.merge([b, zeros, zeros])  # Une el canal azul real con verde y rojo en cero (solo se ve azul).
green_img = cv2.merge([zeros, g, zeros])  # Une el canal verde real con azul y rojo en cero (solo se ve verde).
red_img = cv2.merge([zeros, zeros, r])  # Une el canal rojo real con azul y verde en cero (solo se ve rojo).

cv2.imshow('Canal Azul (Coloreado valeria yaretzi 1341)', blue_img)  # Muestra la imagen filtrada únicamente en color azul.
cv2.imshow('Canal Verde (Coloreado valeria 1341)', green_img)  # Muestra la imagen filtrada únicamente en color verde.
cv2.imshow('Canal Rojo (Coloreado) valeria yaretzi 1341', red_img)  # Muestra la imagen filtrada únicamente en color rojo.
cv2.waitKey(0)  # Espera a que se presione una tecla para avanzar.
# 7. REDIMENSIONAMIENTO DE IMÁGENES (RESIZING)
# ==============================================================================
print("\n7. REDIMENSIONANDO IMÁGENES")  # Imprime el título de la séptima sección.
resized_img = cv2.resize(img_pibble, (400, 300))  # Cambia el tamaño exacto de la imagen a 400px de ancho por 300px de alto.
cv2.imshow('Redimensionada a 400x300', resized_img)  # Muestra la imagen con sus nuevas dimensiones fijas.
cv2.waitKey(0)  # Espera a que se presione una tecla.

half_size = cv2.resize(img_pibble, None, fx=0.5, fy=0.5)  # Reduce la imagen a la mitad (50% en ancho y 50% en alto).
double_size = cv2.resize(img_pibble, None, fx=1.5, fy=1.5)  # Amplía la imagen un 50% extra (escala 1.5x).

cv2.imshow('Mitad de tamano (0.5x) valeria yaretzi 1341', half_size)  # Muestra la versión reducida.
cv2.waitKey(0)  # Espera a que se presione una tecla.
cv2.imshow('Ampliada (1.5x) valeria yaretzi ', double_size)  # Muestra la versión ampliada.
cv2.waitKey(0)  # Espera a que se presione una tecla.
# 8. ROTACIÓN DE IMÁGENES
# ==============================================================================
print("\n8. ROTANDO IMÁGENES")  # Imprime el título de la octava sección.
height, width = img_pibble.shape[:2]  # Obtiene nuevamente el alto y ancho actual de la imagen original.
rotation_matrix = cv2.getRotationMatrix2D((width / 2, height / 2), 45, 1)  # Calcula la matriz para girar 45° desde el centro.
rotated_img = cv2.warpAffine(img_pibble, rotation_matrix, (width, height))  # Aplica la rotación matemática sobre la imagen.

cv2.imshow('Imagen Rotada (45 grados)', rotated_img)  # Muestra la imagen inclinada 45 grados.
cv2.waitKey(0)  # Espera a que se presione una tecla.
# 9. VOLTEO / ESPEJO DE IMÁGENES (FLIPPING)
# ==============================================================================
print("\n9. VOLTEANDO IMÁGENES")  # Imprime el título de la novena sección.
horizontal_flip = cv2.flip(img_pibble, 1)  # Voltea la imagen horizontalmente (código 1 = efecto espejo).
cv2.imshow('Volteo Horizontal (Espejo)', horizontal_flip)  # Muestra el volteo horizontal.
cv2.waitKey(0)  # Espera a que se presione una tecla.

vertical_flip = cv2.flip(img_pibble, 0)  # Voltea la imagen verticalmente (código 0 = de cabeza).
cv2.imshow('Volteo Vertical (De cabeza)', vertical_flip)  # Muestra el volteo vertical.
cv2.waitKey(0)  # Espera a que se presione una tecla.

both_flip = cv2.flip(img_pibble, -1)  # Voltea en ambos ejes al mismo tiempo (código -1 = horizontal + vertical).
cv2.imshow('Volteo en Ambos Ejes', both_flip)  # Muestra el volteo combinado.
cv2.waitKey(0)  # Espera a que se presione una tecla.
# 10. GUARDADO DE RESULTADOS Y LIMPIEZA
# ==============================================================================
print("\n10. GUARDANDO IMAGEN RESULTANTE")  # Imprime el título de la décima sección.
result = cv2.imwrite('rotated_image.jpg', rotated_img)  # Guarda la imagen rotada en el disco duro como 'rotated_image.jpg'.

if result:  # Comprueba si el guardado devolvió True (verdadero).
    print("Imagen rotada guardada exitosamente como 'rotated_image.jpg'")  # Confirma que el archivo se creó.
else:  # Si ocurrió algún problema de permisos o ruta...
    print("Error: No se pudo guardar la imagen rotada.")  # Notifica el fallo en consola.

cv2.destroyAllWindows()  # Cierra todas las ventanas gráficas abiertas por OpenCV para liberar memoria RAM.
print("\n¡Todas las operaciones se completaron con éxito!")  # Mensaje final de cierre en la terminal.