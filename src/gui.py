import src.backend as rd
import PySimpleGUI as sg
import os

def definirTitlebar():
    titlebar = sg.Titlebar(title = "Redimensionador - 1.6 - Iván Azuaje 2023",
    icon = None,
    text_color = "black",
    font = "BlackChancery 10")
    return titlebar


def definirColumna1(dir_imagenes):
    archivos = [[sg.Listbox(values = rd.actualizarListaArchivos(dir_imagenes), key = "elementos", size = (20, 8))]]
    columna1 = [
        [sg.Frame("Archivos", archivos, font="BlackChancery 12", title_color = "white")],
        [sg.Button("Actualizar", pad = (60, 10), font = "BlackChancery 10", size = (12, 2))]
        ]
    return columna1

def definirColumna2(ancho, largo):
    columna2 = [
        [sg.Button("Redimensionar", pad = (10, 5), size = (15, 2), font = "BlackChancery 12" )],
        [sg.Text("Ancho:", pad = (5, 5), font = "BlackChancery 11"), sg.InputText(f"{ancho}", s = (10,1), key = "ancho")],
        [sg.Text("largo:", pad = (5, 10), font = "BlackChancery 11"), sg.InputText(f"{largo}", s = (10,1), key = "largo")],
        [sg.Button("Salir :(", pad = (10, 20),button_color=('white', 'firebrick3'), font = "BlackChancery 12")],
        ]
    return columna2

def definirVentana(dir_imagenes, ancho, largo):
    columna1 = definirColumna1(dir_imagenes)
    columna2 = definirColumna2(ancho, largo)
    titlebar = definirTitlebar()
    layout = [
        [titlebar],
        [sg.Text("Redimensionador", pad = (100,1),
                 justification = "center", font = "BlackChancery 22",
                 text_color = "white")
         ],
        [sg.Text('_'*56)],
        [sg.Column(columna1), sg.VSeperator(), sg.Column(columna2)],
        [sg.Text('_'*56)],
        [sg.Text("Desarrollado por Iván Azuaje Ayala - 2023", pad = (70, 2), font = "BlackChancery 12")],
        [sg.Text("V1.6", font = "Any 6")]
        ]
    return layout

def event_loop(ventana, dir_imagenes, dir_redimension):
    while(True):
        evento, valores = ventana.read()
        
        if evento == "Actualizar":
            ventana["elementos"].update(rd.actualizarListaArchivos(dir_imagenes))
            
        elif evento == "Redimensionar":

            _ancho = rd.validarDatos(valores["ancho"])
            _largo = rd.validarDatos(valores["largo"])
            if (_ancho == 0 or _largo == 0):
                sg.popup_error("Error, hay algo raro en las dimensiones...", title = "Error", font = "BlackChancery 10")
                continue

            rd.llamar_acto(_ancho, _largo, dir_imagenes, dir_redimension)
            cantidad = len(os.listdir(f"{dir_imagenes}"))
            sg.popup(f"Se han redimensionado {cantidad} archivos.", title = "Éxito", font = "BlackChancery 10")
        #========================================================================================
        elif evento == "Salir :(" or evento == sg.WIN_CLOSED:
            break
    ventana.close()

def iniciarGUI():
    sg.theme('Dark Amber')
    ancho, largo, dir_imagenes, dir_redimension = rd.leer_config()
    #===========================================================================#
    layout = definirVentana(dir_imagenes, ancho, largo)
    #===========================================================================#
    ventana = sg.Window("REDIMENSIONADOR", layout, margins=(10,10))
    
    event_loop(ventana, dir_imagenes, dir_redimension)

def preview():
    sg.theme_previewer()