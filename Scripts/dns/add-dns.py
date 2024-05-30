# Definir la línea que queremos añadir
import sys
import subprocess
import pickle


fileObja = open('/etc/bind/zonas/bdd.obj', 'rb')
dic = pickle.load(fileObja)
fileObja.close()


serv_name = sys.argv[1]
puerto = sys.argv[2]

linea_a_anadir = f"{serv_name} IN A 10.1.82.174"
linea_a_anadir2 = f"_minecraft._tcp.{serv_name} IN SRV 0 0 {puerto} {serv_name}.dominexhosting.es."

# Nombre del archivo
nombre_archivo = "/etc/bind/zonas/db.dominex"

try:
    # Abrir el archivo en modo append (añadir)
    with open(nombre_archivo, "a") as archivo:
        # Añadir la línea al final del archivo
        archivo.write(linea_a_anadir + "\n")
    print(f"Línea añadida exitosamente al archivo {nombre_archivo}.")
#    comando_reload = "systemctl reload bind9"
#    output = subprocess.run(comando_reload, shell=True, capture_output=True, text=True)


except Exception as e:
    print(f"Error al intentar añadir la línea al archivo: {e}")


try:
    # Abrir el archivo en modo append (añadir)
    with open(nombre_archivo, "a") as archivo:
        # Añadir la línea al final del archivo
        archivo.write(linea_a_anadir2 + "\n")
    print(f"Línea añadida exitosamente al archivo {nombre_archivo}.")
    # Reiniciamos servicio
    comando_reload = "sudo systemctl reload bind9"
    output = subprocess.run(comando_reload, shell=True, capture_output=True, text=True)

    # Actualizamos DNS Master-Slave

    #ssh slave@192.168.10.61 'sudo rm /var/cache/bind/*
    comando_rm = dic["sshrm"]
    output = subprocess.run(comando_rm, shell=True, capture_output=True, text=True)
    #ssh slave@192.168.10.61 'sudo systemctl restart bind9'
    comando_restart = dic["sshrestart"]
    output = subprocess.run(comando_restart, shell=True, capture_output=True, text=True)

except Exception as e:
    print(f"Error al intentar añadir la línea al archivo: {e}")
