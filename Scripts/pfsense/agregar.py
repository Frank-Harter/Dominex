#!/usr/bin/env python3
import fileinput
import sys
import subprocess

puerto = sys.argv[1]

# Texto que quieres añadir
texto_a_anadir = f'''<!--ID_{puerto}_-->
                 <rule>
                        <source>
                                <any></any>
                        </source>
                        <destination>
                                <network>wanip</network>
                                <port>{puerto}</port>
                        </destination>
                        <ipprotocol>inet</ipprotocol>
                        <protocol>tcp</protocol>
                        <target>192.168.10.30</target>
                        <local-port>{puerto}</local-port>
                        <interface>wan</interface>
                        <descr></descr>
                        <associated-rule-id>nat_662a1aa0da8478.04662297</associated-rule-id>
                        <updated>
                                <time>1714035360</time>
                                <username><![CDATA[admin@10.1.82.11 (Local Database)]]></username>
                        </updated>
                        <created>
                                <time>1714035360</time>
                                <username><![CDATA[admin@10.1.82.11 (Local Database)]]></username>
                        </created>
                </rule>
'''

# Ruta del archivo
ruta_archivo = "/cf/conf/config.xml"

# Modificar el archivo para insertar el texto después de la línea especificada
inserted = False
for line in fileinput.input(ruta_archivo, inplace=True):
    sys.stdout.write(line)  # Escribir la línea original
    if '<separator></separator>' in line and not inserted:
        sys.stdout.write(texto_a_anadir)  # Escribir el texto después de la línea especificada
        inserted = True

if not inserted:
    print("La etiqueta <separator></separator> no fue encontrada en el archivo.")

print("Texto añadido correctamente al archivo config.xml.")



# Ejecutar el comando
command = 'rm /tmp/config.cache'
subprocess.run(command.split())
# Ejecutar el comando
command = 'php /rec.php'
subprocess.run(command.split())
