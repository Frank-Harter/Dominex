import sys
import subprocess
import pickle

fileObja = open('/etc/bind/zonas/bdd.obj', 'rb')
dic = pickle.load(fileObja)
fileObja.close()


# Definir el subdominio que queremos usar para borrar la línea
subdominio_a_borrar = sys.argv[1]

# Lineas que queremos buscar y borrar
patron_a_borrar = f"{subdominio_a_borrar} IN"
patron_a_borrar2 = f"_minecraft._tcp.{subdominio_a_borrar} IN"

# Nombre del archivo
nombre_archivo = "/etc/bind/zonas/db.dominex"

try:
    # Leer todas las líneas del archivo
    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()

    # Linea por linea busca algun patron de los que buscamos (se podria decir que esto es un grep)
    lineas_modificadas = [linea for linea in lineas if patron_a_borrar not in linea]

    # Escribir las líneas modificadas de nuevo en el archivo
    with open(nombre_archivo, "w") as archivo:
        archivo.writelines(lineas_modificadas)


    print(f"Líneas que contienen el subdominio {subdominio_a_borrar} borradas exitosamente del archivo {nombre_archivo}.")
except Exception as e:
    print(f"Error al intentar borrar la línea del archivo: {e}")


try:
    # Leer todas las líneas del archivo
    with open(nombre_archivo, "r") as archivo:
        lineas = archivo.readlines()

    # Filtrar las líneas, eliminando cualquier línea que contenga el patrón especificado
    lineas_modificadas = [linea for linea in lineas if patron_a_borrar2 not in linea]

    # Escribir las líneas modificadas de nuevo en el archivo
    with open(nombre_archivo, "w") as archivo:
        archivo.writelines(lineas_modificadas)

    # Reiniciamos para que se apliquen los cambios
    comando_reload = "sudo systemctl reload bind9"
    output = subprocess.run(comando_reload, shell=True, capture_output=True, text=True)

    #ssh slave@192.168.10.61 'sudo rm /var/cache/bind/*
    comando_rm = dic["sshrm"]
    output = subprocess.run(comando_rm, shell=True, capture_output=True, text=True)

    # ssh slave@192.168.10.61 'sudo systemctl restart bind9'
    comando_restart = dic["sshrestart"]
    output = subprocess.run(comando_restart, shell=True, capture_output=True, text=True)



    print(f"Líneas que contienen el subdominio {subdominio_a_borrar} borradas exitosamente del archivo {nombre_archivo}.")
except Exception as e:
    print(f"Error al intentar borrar la línea del archivo: {e}")
