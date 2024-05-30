#!/usr/bin/env python3
import fileinput
import sys
import subprocess

# Ruta del archivo
ruta_archivo = "/cf/conf/config.xml"

# Solicitar al usuario que ingrese el número identificador
id_numero = sys.argv[1]

# Preparar el comentario del identificador a buscar
id_comentario = f"<!--ID_{id_numero}_-->"

# Variables para controlar la impresión de líneas
skip = False

# Procesar el archivo para eliminar la regla específica
for line in fileinput.input(ruta_archivo, inplace=True):
    if id_comentario in line:
        skip = True  # Comenzar a saltar líneas desde el comentario identificador
        continue  # También saltar la línea del comentario
    if skip:
        if '</rule>' in line:
            skip = False  # Dejar de saltar líneas después de cerrar la etiqueta de la regla
            continue  # No imprimir la línea de cierre de la regla
        else:
            continue  # Seguir saltando líneas dentro de la regla

    sys.stdout.write(line)  # Escribir líneas que no están dentro de la regla a eliminar

print(f"La regla con ID {id_numero} ha sido eliminada correctamente del archivo.")
# Ejecutar el comando
command = 'rm /tmp/config.cache'
subprocess.run(command.split())
# Ejecutar el comando
command = 'php /rec.php'
subprocess.run(command.split())
