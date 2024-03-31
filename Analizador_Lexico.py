import re
from archivo import *

tokens = [
    ('Llave abrir', r'\{'),
    ('Llave cerrar', r'\}'),
    ('Dos puntos', r'\:'),
    ('Cadena', r'\"[^\"]*\"'),
    ('Espacios', r'\s+') #* Token para ignorar los espacios en blanco
]

#! Funcion del Analizador Lexico

def analizador_lexico(archivo):
    global lista_tokens_no_validos
    global lista_tokens_validos
    lista_tokens_validos = []
    lista_tokens_no_validos = []
    num_linea = 1 
    num_columna = 1

    while archivo:
        tokenencontrado = False

        for token_nom, patron_exp in tokens:
            patron = re.compile(patron_exp)
            considencia = patron.match(archivo)

            if considencia:
                valor = considencia.group(0)
                if token_nom != 'Espacios':
                    lista_tokens_validos.append((token_nom, valor, num_linea, num_columna))
                tokenencontrado = True
                archivo = archivo[len(valor):]
                num_columna += len(valor)
                break

        if not tokenencontrado:
            lista_tokens_no_validos.append(('Caracter no valido', archivo[0], num_linea, num_columna))
            archivo = archivo[1:]
            num_columna += 1
        
        if archivo and archivo[0] == '\n':
            num_linea += 1
            num_columna = 1 
            archivo = archivo[1:]

    return lista_tokens_validos, lista_tokens_no_validos

'''def analizador_lexico(archivo):
    global lista_tokens
    lista_tokens = []
    num_linea = 1 
    num_columna = 1

    while archivo:
        tokenencontrado = False

        for token_nom, patron_exp in tokens:
            patron =  re.compile(patron_exp)
            considencia = patron.match(archivo)

            if considencia:
                valor = considencia.group(0)
                if token_nom != 'Espacios':
                    lista_tokens.append((token_nom, valor, num_linea, num_columna))
                tokenencontrado = True
                archivo = archivo[len(valor):]
                num_columna += len(valor)
                break

        if not tokenencontrado:
            lista_tokens.append(('Caracter no valido', archivo[0], num_linea, num_columna))
            archivo = archivo[1:]
            num_columna += 1
        
        if archivo and archivo[0] == '\n':
            num_linea += 1
            num_columna = 1 
            archivo = archivo[1:]

    return lista_tokens'''

def generar_tabla_html():
    global tabla_html, tabla_html_novalidos
    tabla_html = '<div style="margin: 0 auto; width: fit-content;">\n'
    tabla_html += '<div style="text-align: center;"><h2>Tabla de Tokens Válidos</h2></div>\n'
    tabla_html += '<table border="1">\n'
    tabla_html += '<tr><th>Token</th><th>Lexema</th><th>Número de línea</th><th>Número de columna</th></tr>\n'

    tabla_html_novalidos = '<div style="margin: 0 auto; width: fit-content;">\n'
    tabla_html_novalidos += '<div style="text-align: center;"><h2>Tabla de Caracteres No Válidos</h2></div>\n'
    tabla_html_novalidos += '<table border="1">\n'
    tabla_html_novalidos += '<tr><th>Carácter</th><th>Número de línea</th><th>Número de columna</th></tr>\n'

    for token in lista_tokens_validos:
        tabla_html += f'<tr><td>{token[0]}</td><td>{token[1]}</td><td>{token[2]}</td><td>{token[3]}</td></tr>\n'

    for token_no_v in lista_tokens_no_validos:
        tabla_html_novalidos += f'<tr><td>{token_no_v[1]}</td><td>{token_no_v[2]}</td><td>{token_no_v[3]}</td></tr>\n'

    tabla_html += '</table>\n</div>\n'
    tabla_html_novalidos += '</table>\n</div>\n'
    return tabla_html, tabla_html_novalidos

def generar_archivo_html():
    with open("C:/Users/danis/OneDrive/Documents/Quinto Semestre/LFP/Proyecto1[LFP]/tabla_tokens.html", "w") as archivo:
        archivo.write("<!DOCTYPE html>\n")
        archivo.write("<html>\n<head>\n<title>Tabla de Tokens</title>\n</head>\n<body>\n")
        archivo.write(tabla_html)
        archivo.write(tabla_html_novalidos)
        archivo.write("\n</body>\n</html>")
