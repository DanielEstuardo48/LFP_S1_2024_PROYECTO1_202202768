import tkinter
import tkinter.filedialog
import json
import html
from tkinter import messagebox
from tkinter import ttk
from Analizador_Lexico import *

# #*Se crea la ventana 
win = tkinter.Tk()
win.title("Proyecto 1 [LFP]")
win.configure(background='#F89027')
win.geometry("850x750+430+20")

archivo = None

def abrir_archivo():
    global archivo
    archivo = tkinter.filedialog.askopenfilename(initialdir="C:/Users/danis/OneDrive/Documents/Quinto Semestre/LFP/Proyecto1[LFP]", title="Explorador")
    if archivo:
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                global datos
                datos = file.read()  # Leer el contenido del archivo
                text_widget.delete(1.0, tkinter.END)  # Limpiar el widget de texto
                text_widget.insert(tkinter.END, datos)  # Insertar los datos en el widget de texto
        except Exception as e:
            print("Error al cargar archivo:", e)


def traductor(archivo):
    html_resultado = '<!DOCTYPE html>\n<html lang="es">\n<head>\n<meta charset="utf-8">\n<meta name="viewport" content="width=device-width, initial-scale=1.0">\n<title>{}</title>\n</head>\n<body>\n\n'.format(archivo["Inicio"]["Encabezado"]["TituloPagina"])

    for elemento in archivo["Cuerpo"]:
        for etiqueta, contenido in elemento.items():
            if etiqueta == "Titulo":
                tamaño_titulo = ""
                if contenido["tamaño"] == "t1":
                    tamaño_titulo = "22px"
                elif contenido["tamaño"] == "t2":
                    tamaño_titulo = "20px"
                elif contenido["tamaño"] == "t3":
                    tamaño_titulo = "18px"
                elif contenido["tamaño"] == "t4":
                    tamaño_titulo = "16px"
                elif contenido["tamaño"] == "t5":
                    tamaño_titulo = "14px"
                elif contenido["tamaño"] == "t6":
                    tamaño_titulo = "12px"
                html_resultado += '<div style="text-align: {};"><h1 style="color: {}; font-size: {}">{}</h1></div>\n'.format(contenido["posicion"].replace("derecha", "right").replace("izquierda", "left").replace("centro", "center"), contenido["color"].replace("rojo", "red").replace("amarillo", "yellow").replace("azul", "blue"), tamaño_titulo,  html.escape(contenido["texto"]))  # Escapar caracteres especiales
            elif etiqueta == "Fondo":
                html_resultado += '<body style="background-color: {};">\n'.format(contenido["color"].replace("rojo", "red").replace("amarillo", "yellow").replace("azul", "blue"))
            elif etiqueta.startswith("Parrafo"):
                html_resultado += '<p style="text-align: {};">{}</p>\n'.format(contenido["posicion"].replace("derecha", "right").replace("izquierda", "left").replace("centro", "center"), html.escape(contenido["texto"]))  # Escapar caracteres especiales
            elif etiqueta.startswith("Texto"):
                html_resultado += '<p style="font-family: {}; color: {}; font-size: {}px;">Texto</p>\n'.format(contenido["fuente"], contenido["color"].replace("rojo", "red").replace("amarillo", "yellow").replace("azul", "blue"), contenido["tamaño"])
            elif etiqueta == "Codigo":
                html_resultado += '<div style="text-align: {};">\n<code>{}</code>\n</div>\n'.format(contenido["posicion"].replace("derecha", "right").replace("izquierda", "left").replace("centro", "center"), html.escape(contenido["texto"]))  # Escapar caracteres especiales
            elif etiqueta == "Negrita":
                html_resultado += '<strong>{}</strong>\n'.format(html.escape(contenido["texto"]))
            elif etiqueta == "Subrayado":
                html_resultado += '<u>{}</u>\n'.format(html.escape(contenido["texto"]))
            elif etiqueta == "Tachado":
                html_resultado += '<s>{}</s>\n'.format(html.escape(contenido["texto"]))
            elif etiqueta == "Cursiva":
                html_resultado += '<em>{}</em>\n'.format(html.escape(contenido["texto"]))
            elif etiqueta == "Salto":
                html_resultado += '<br>' * int(contenido["cantidad"]) + '\n'
            elif etiqueta.startswith("Tabla"):
                html_resultado += '<table style="border-collapse: collapse;">\n'
                tabla_data = contenido
                filas = int(tabla_data["filas"])
                columnas = int(tabla_data["columnas"])
                elementos = tabla_data["elemento"]
                
                for fila in range(filas):
                    html_resultado += '<tr>\n'
                    for columna in range(columnas):
                        html_resultado += '<td style="border: 1px solid black; padding: 5px;">'
                        for elemento_tabla in elementos:
                            if int(elemento_tabla["fila"]) == fila + 1 and int(elemento_tabla["columna"]) == columna + 1:
                                html_resultado += html.escape(elemento_tabla["texto"]) + '<br>'
                        html_resultado += '</td>'
                    html_resultado += '</tr>\n'
                
                html_resultado += '</table>\n'


        if "Fondo" in elemento.keys():
            html_resultado += '</div>\n'
    html_resultado += '</body>\n</html>'
    return html_resultado


def generarhtml():
    if archivo:
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                archivo_data = json.loads(file.read())  # Cargar el contenido del archivo como un JSON
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar el archivo JSON: {e}")
            return

        html_output = ""
        try:
            html_output = traductor(archivo_data)
        except Exception as e:
            messagebox.showerror("Error", f"Error al generar la traducción HTML: {e}")
            index = str(e).find("position ") + 9
            error_index = int(str(e)[index:])
            try:
                html_output = traductor(archivo_data[:error_index])
            except:
                pass

        try:
            with open("C:/Users/danis/OneDrive/Documents/Quinto Semestre/LFP/Proyecto1[LFP]/resultado.html", "w", encoding='utf-8') as file:
                file.write(html_output)
            text_widgethtml.delete(1.0, tkinter.END)  # Limpiar el widget de texto
            text_widgethtml.insert(tkinter.END, html_output)
            messagebox.showinfo("Info", "El archivo HTML se ha creado con éxito.")
        except Exception as e:
            messagebox.showerror("Error", f"Error al escribir el archivo HTML: {e}")
    else:
        messagebox.showwarning("Advertencia", "Por favor, abre un archivo primero.")

def abrir_archivo_y_analizar():
    global archivo
    abrir_archivo()
    if archivo:
        try:
            with open(archivo, 'r', encoding='utf-8') as file:
                archivo_data = file.read()
                lista_tokens_validos = analizador_lexico(archivo_data)
                lista_tokens_no_validos = analizador_lexico(archivo_data)
        except Exception as e:
            print("Error al abrir el archivo:", e)

def traducir_archivo_y_tabla():
    generarhtml()
    generar_tabla_html()

# !Se agregan los textos de bienvenida y todo el cuerpo de la pagina

# *Este es el marco
frame = tkinter.Frame(win, bg="black", bd=2, relief="solid", width=200, height=50, padx=3, pady=3)
frame.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# *Este es el texto 
label = tkinter.Label(frame, text=" Bienvenido al traductor ", font=("Calibri", 24, "bold"), fg="black")
label.pack()

# *Se crea un lienzo para el texto
lienzo = tkinter.Canvas(win, width=frame.winfo_width(), height=frame.winfo_height())
lienzo.place(relx=0.5, rely=0.1, anchor=tkinter.CENTER)

# *Se crea el boton
button = ttk.Button(text="Abrir archivo", cursor="hand2", command=abrir_archivo_y_analizar,style='Estilo.TButton')
button.place(x=25, y=130)

#* Se crea el espacio enblanco para el texto

label_entra = tkinter.Label(win, text="Texto de entrada:", fg="black", bg="#F89027", font=("Arial", 10))
label_entra.place(x=25, y=170)

#!Estilo de boton
style = ttk.Style()
style.configure('Estilo.TButton', foreground='black', font=('Helvetica', 12, 'bold'))

buttonA = ttk.Button(text="Traducir", cursor="hand2",command=traducir_archivo_y_tabla, style='Estilo.TButton')
buttonA.place(x=370,y=700)

#! Espacio para el texto de entrada
text_widget = tkinter.Text(win, wrap=tkinter.WORD)
text_widget.pack(expand=True, fill=tkinter.Y)
text_widget.config(width=47, height=30)
text_widget.place(x=25, y=190)

#! Espacio para el texto de salida

label_salida = tkinter.Label(win, text="Traducción:", fg="black", bg="#F89027", font=("Arial", 10))
label_salida.place(x=445, y=170)

text_widgethtml = tkinter.Text(win, wrap=tkinter.WORD)
text_widgethtml.pack(expand=True, fill=tkinter.Y)
text_widgethtml.config(width=47, height=30)
text_widgethtml.place(x=445, y=190)


#! Boton para tabla de analizador

buttonL = ttk.Button(text="Tablas de analizador", cursor="hand2",command=generar_archivo_html, style='Estilo.TButton')
buttonL.place(x=445,y=130)

win.mainloop()