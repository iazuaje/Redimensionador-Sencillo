import os
import cv2
import numpy as np
import shutil
import PySimpleGUI as sg

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
    contador = 1
    for imagen in archivo:
        sg.one_line_progress_meter('Redimensionando', contador, len(archivo), 'Por favor','Aguarda un segundo')
        img = cv2.imread(f"{dir1}/{imagen}")
        dimensiones = img.shape
        #alto = conseguir_altura(dimensiones, largo)
        res = cv2.resize(img, dsize = (largo, alto), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite(f"{dir2}/{imagen}", res, [cv2.IMWRITE_JPEG_QUALITY,100])
        contador+= 1
        
def conseguir_altura(dimensiones, l_original):
    return round((l_original/dimensiones[1])*dimensiones[0])

def llamar_acto(largo, alto, dir_imagenes, dir_redimension):
    archivos = conseguir_ficheros(dir_imagenes)
    redimensionar(archivos, dir_imagenes, dir_redimension, int(largo), int(alto))
    
#======================================GRAFICOS====================================#
def actualizarListaArchivos(direccion):
    lista = []
    archivos = conseguir_ficheros(direccion)
    for imagen in archivos:
        lista.append(imagen)
    return lista
    
def mainGrafico():
    sg.theme('Dark Grey 13')
    largo, alto, dir_imagenes, dir_redimension = leer_config()
    archivos = [[sg.Listbox(values = actualizarListaArchivos(dir_imagenes), key = "elementos", size = (20, 8))]]
    #===========================================================================#
    
    columna1 = [
        [sg.Frame("Archivos", archivos, font="BlackChancery 12", title_color = "blue")],
        [sg.Button("Actualizar", pad = (60, 10), font = "BlackChancery 10", size = (12, 2))]
        ]
    columna2 = [
        [sg.Button("Redimensionar", pad = (10, 50), size = (15, 2), font = "BlackChancery 12" )],
        [sg.Button("Configuración", pad = (10, 20), font = "BlackChancery 12")],
        [sg.Button("Salir :(", pad = (10, 0),button_color=('white', 'firebrick3'), font = "BlackChancery 12")],
        ]
    
    layout = [
        [sg.Text("Redimensionador", pad = (100,10),
                 justification = "center", font = "BlackChancery 22",
                 text_color = "white")
         ],
        [sg.Text('_'*56)],
        [sg.Column(columna1), sg.VSeperator(), sg.Column(columna2)],
        [sg.Text('_'*56)],
        [sg.Text("Desarrollado por Iván Azuaje Ayala - 2022", pad = (70, 2), font = "BlackChancery 12")],
        [sg.Text("V1.4", font = "Any 6")]
        ]
    
    #===========================================================================#
    
    ventana = sg.Window("REDIMENSIONADOR", layout, margins=(10,10))
    
    #EVENT LOOOOPP ===========================
    while(True):
        evento, valores = ventana.read()
        
        if evento == "Actualizar":
            ventana["elementos"].update(actualizarListaArchivos(dir_imagenes))
            
        elif evento == "Redimensionar":
            llamar_acto(largo, alto, dir_imagenes, dir_redimension)
            cantidad = len(os.listdir(f"{dir_imagenes}"))
            sg.popup(f"Se han redimensionado {cantidad} archivos.", font = "BlackChancery 10")
        #========================================================================================
        elif evento == "Configuración":
            texto = sg.popup_get_text(f'Dimensiones: {largo}x{alto}', 'Configurar:', font = "BlackChancery 10")
            if texto != None:
                textDimensiones = texto.split()
            else:
                textDimensiones = [None,None]
            try:
                if textDimensiones[0].isnumeric() and 300 <= int(textDimensiones[1]) <= 2400:
                    largo = int(textDimensiones[0])
                else:
                    sg.popup("ERROR\n introduciste algo mal. Procura escribir '1280 720'", font = "BlackChancery 10")
            except:
                pass
            try:
                if textDimensiones[1].isnumeric() and 300 <= int(textDimensiones[1]) <= 2400:
                    alto = int(textDimensiones[1])
                else:
                    sg.popup("ERROR\n introduciste algo mal. Procura escribir '1280 720'", font = "BlackChancery 10")
            except:
                pass
        #Terminar el programa si se cierra la ventana o la persona le da ok
        elif evento == "Salir :(" or evento == sg.WIN_CLOSED:
            break
    ventana.close()
    
mainGrafico()          