import sys

def main():
    # Verificar si se pasó un argumento al script
    if len(sys.argv) < 2:
        print("Por favor, pasa una VARIABLE como argumento al ejecutar el script.")
        sys.exit(1)  # Salir del script porque no se proporcionó el argumento necesario

    # Leer el argumento pasado al script
    par_1 = sys.argv[1]
    nombre_pvc = par_1
    service_name = par_1
    nombre_pv = par_1
    nombre_pod = par_1
    nombre_volumen = par_1
    print(f"Has introducido: {service_name}")
    print(f"Has introducido: {nombre_pvc}")


    # Texto YAML con placeholders para ser reemplazados por la variable 'service_name'
    yaml_content = f"""
apiVersion: v1
kind: PersistentVolume
metadata:
  name: {nombre_pv}
spec:
  capacity:
    storage: 10Gi
  volumeMode: Filesystem
  accessModes:
    - ReadWriteOnce
  persistentVolumeReclaimPolicy: Retain
  hostPath:
    path: /mnt/alejandro

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
      storage: 10Gi

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
        ports:
        - containerPort: 25565
        volumeMounts:
        - name: {nombre_volumen}
          mountPath: /data
        resources:
          requests:
            memory: "1Gi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "1000m"
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
      nodePort: 30003  # Aquí especificamos el puerto NodePort
  selector:
    app: {nombre_pod}

"""

    # Crear archivo YAML con el nombre de servicio personalizado
    with open('archivo.yaml', 'w') as file:
        file.write(yaml_content)

    print("archivo.yaml ha sido creado con éxito con el nombre del servicio personalizado.")

if __name__ == "__main__":
    main()

