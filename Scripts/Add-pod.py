import sys
import pymysql
import subprocess
import pickle

argumentos = len(sys.argv)

if argumentos != 4:
    print("Argumentos incorrectos")
    sys.exit(1)
else:
    print("Argumentos Correctos")

par_1_user = sys.argv[1] # Nombre de usuario
par_2_servername = sys.argv[2].lower() # Nombre del servidor
nombre_pvc = par_2_servername
service_name = par_2_servername
nombre_pv = par_2_servername
nombre_pod = par_2_servername
nombre_volumen = par_2_servername


dic = {       'password':"Super3ies1234.",
                'hostbdd':"192.168.10.90", 'puertobdd':3307, 'userbdd':"admin", 'databdd':"FDominex",
                'sshpfsense':"ssh -i /home/master/.ssh/id_rsa_new admin@192.168.10.1 'python3.11 /a.py ",
                'sshdns':"ssh -i /home/master/.ssh/dnss master@192.168.10.60 'python3 /etc/bind/zonas/add-dns.py "
}
fileObj = open('master.obj', 'wb')
pickle.dump(dic,fileObj)
fileObj.close()


fileObja = open('/home/master/SCRIPTS/master.obj', 'rb')
dic = pickle.load(fileObja)
fileObj.close()



par_3_plan = sys.argv[3] # Dependiendo del plan de que nos llegue asignaremos unos recursos
if par_3_plan == "Iniciante":
    cpu = "500"
    ram = "2"
    almacenamiento = "5"
elif par_3_plan == "Aficionado":
    cpu = "1000"
    ram = "4"
    almacenamiento = "13"
elif par_3_plan == "Avanzado":
    cpu = "2000"
    ram = "8"
    almacenamiento = "18"

try:
    conn = pymysql.connect(host=dic["hostbdd"], port=dic["puertobdd"], user=dic["userbdd"], password=dic["password"], db=dic["databdd"], charset='utf8mb4')
    with conn.cursor() as cursor:
        # Realizar una consulta
        sql = """SELECT MAX(puerto) + 1 from servidores"""
        cursor.execute(sql) #Ejecutar Consulta
        resultado_celda = cursor.fetchone()  # Esto devuelve una celda con un dato
        if resultado_celda: #Si existe algun resultado
            next_port = str(resultado_celda[0])
        else:
            print("No se encontraron registros.")
finally:
    conn.close()


def main():
    global id_pod

    # YAML para el servidor de minecraft.
    yaml_content = f"""
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {nombre_pv}
spec:
  capacity:
    storage: {almacenamiento}Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/samba/clientes/.{par_1_user}/{nombre_pod}

---

apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: {nombre_pvc}
spec:
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: {almacenamiento}Gi

---

apiVersion: apps/v1
kind: Deployment
metadata:
  name: {nombre_pod}
spec:
  replicas: 1
  selector:
    matchLabels:
      app: {nombre_pod}
  template:
    metadata:
      labels:
        app: {nombre_pod}
    spec:
      containers:
      - name: minecraft-contenedor
        image: itzg/minecraft-server
        env:
        - name: EULA
          value: "TRUE"
        - name: MEMORY
          value: "{ram}G"
        - name: ONLINE_MODE
          value: "false"
        ports:
        - containerPort: 25565
        volumeMounts:
        - name: {nombre_volumen}
          mountPath: /data
        resources:
          requests:
            memory: "{ram}Gi"
            cpu: "{cpu}m"
          limits:
            memory: "{ram}Gi"
            cpu: "{cpu}m"
      volumes:
      - name: {nombre_volumen}
        persistentVolumeClaim:
          claimName: {nombre_pvc}

---

apiVersion: v1
kind: Service
metadata:
  name: {service_name}
spec:
  type: NodePort
  ports:
    - port: 25565
      targetPort: 25565
      nodePort: {next_port}  # Aquí especificamos el puerto NodePort
  selector:
    app: {nombre_pod}

"""

    # Crear archivo YAML con el nombre del deployment personalizado
    with open('/mnt/samba/yamls/'+nombre_pod+'.yaml', 'w') as file:
        file.write(yaml_content)

    print("archivo.yaml ha sido creado con éxito con el nombre del servicio personalizado.")
    exec_contenedor = "kubectl apply -f  /mnt/samba/yamls/"+nombre_pod+".yaml"
    #Ejecutamos el .yaml (se inicia pod/servidor de minecraft)
    subprocess.run(exec_contenedor, shell=True)

    #Conseguimos nombre del pod
    comando_id_pod = 'kubectl get pods -o wide |grep "^'+nombre_pod+'-" |cut -d" " -f1'
    output = subprocess.run(comando_id_pod, shell=True, capture_output=True, text=True)
    id_pod = output.stdout.strip()

    #Abrimos puerto en el PFSENSE del servidor
    #ssh -i /home/master/.ssh/id_rsa_new admin@192.168.10.1 'python3.11 /a.py next_port
    comando_pfsense = dic["sshpfsense"]+str(next_port)+"'"
    output = subprocess.run(comando_pfsense, shell=True, capture_output=True, text=True)

    # Agregamos el SRV y el subdominio al server DNS
    # ssh -i /home/master/.ssh/dnss master@192.168.10.60 'python3 /etc/bind/zonas/add-dns.py next_port
    comando_dns =  dic["sshdns"]+nombre_pod +" "+str(next_port)+"'"
    output = subprocess.run(comando_dns, shell=True, capture_output=True, text=True)


if __name__ == "__main__": # Nos aseguramos que este script sea el que inicia todo
    main()
try:
    # Metemos los datos en la BDD
    conn = pymysql.connect(host=dic["hostbdd"], port=dic["puertobdd"], user=dic["userbdd"], password=dic["password"], db=dic["databdd"], charset='utf8mb4')
    with conn.cursor() as cursor:
        # Realizar un insert para meter el servidor en la BDD
        insert = """INSERT INTO FDominex.servidores
        (dominio, username, puerto, pod_name, tipo_plan, ruta, status, fecha_creacion)
            VALUES('"""+nombre_pod+"""', '"""+par_1_user+"""','"""+next_port+"""', '"""+id_pod+"""', '"""+par_3_plan+"""', '"""+par_1_user+'/'+nombre_pod+"""', 0, CURRENT_TIMESTAMP);"""
        cursor.execute(insert)
        conn.commit()

        # Metemos la factura
        insert2 = """INSERT INTO FDominex.facturas(username, tipo_plan, paytime, dominio)VALUES('"""+par_1_user+"""', '"""+par_3_plan+"""', CURRENT_TIMESTAMP, '"""+par_2_servername+"""');"""
        cursor.execute(insert2)
        conn.commit()


finally:
    conn.close()
