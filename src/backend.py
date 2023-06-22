import os 
import shutil
import cv2
import numpy as np

def leer_linea(linea):
    preparada = linea.strip("\n").split("=")
    return preparada[1]

def leer_config():
    dimensiones = [1280, 720, "", ""]
    try:
        texto = open("configuracion.txt","r")
        for i in range(len(dimensiones)):
            dimensiones[i] = leer_linea(texto.readline())
    except:
        #input("No hay archivo de configuración! Se aplicarán las opciones por defecto. ")
        texto = open("configuracion.txt", "w")
        texto.write(f"Largo={dimensiones[0]}\n")
        texto.write(f"Alto={dimensiones[1]}\n")
        dir1 = os.getcwd()
        dir1 = dir1.replace("\\","/")
        texto.write(f"directorio imagenes={dir1}/imagenes\n")
        texto.write(f"directorio redimension={dir1}/redimensionadas\n")
        dimensiones = [1200, 720, f"{dir1}/imagenes", f"{dir1}/redimensionadas"]
    texto.close()
    return dimensiones

def conseguir_ficheros(direccion_total):
    ficheros = os.listdir(f"{direccion_total}")
    imagenes = []
    for fichero in ficheros:
        if fichero.endswith('.jpg') or fichero.endswith('.png'):
            imagenes.append(fichero)
    return imagenes

def copiar_archivos(lista, dir1):
    for elemento in lista:
        shutil.copy(f"imagenes/{dir1}/{elemento}", f"redimensionadas/{elemento}")

def redimensionar(archivo, dir1, dir2, largo, alto):
    for imagen in archivo:
        img = cv2.imread(f"{dir1}/{imagen}")
        dimensiones = img.shape
        res = cv2.resize(img, dsize = (largo, alto), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f"{dir2}/{imagen}", res, [cv2.IMWRITE_JPEG_QUALITY,100])
        
def conseguir_altura(dimensiones, l_original):
    return round((l_original/dimensiones[1])*dimensiones[0])

def llamar_acto(largo, alto, dir_imagenes, dir_redimension):
    archivos = conseguir_ficheros(dir_imagenes)
    redimensionar(archivos, dir_imagenes, dir_redimension, int(largo), int(alto))

def actualizarListaArchivos(direccion):
    lista = []
    archivos = conseguir_ficheros(direccion)
    for imagen in archivos:
        lista.append(imagen)
    return lista

def validarDatos(cadenaDeTexto):
    nuevaCadena = ""
    for letra in cadenaDeTexto:
        if letra.isnumeric():
            nuevaCadena += letra
    if len(nuevaCadena) == 0 or (int(nuevaCadena) <= 0 or int(nuevaCadena) > 4000):
        return 0
    else:
        return nuevaCadena