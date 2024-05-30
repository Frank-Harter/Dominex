import yaml
import sys
import subprocess


argumentos = len(sys.argv)

if argumentos < 2:
    print("Argumentos incorrectos")
    sys.exit(1)
else:
    print("Argumentos Correctos")


serv = sys.argv[1]

# Nombre del archivo YAML
filename = f'/mnt/samba/yamls/{serv}.yaml'

estado = sys.argv[2]

# Cargar el archivo YAML
with open(filename, 'r') as file:
    yaml_content = list(yaml.safe_load_all(file))

# Modificar el valor de replicas
for document in yaml_content:
    if document.get('kind') == 'Deployment':
        if 'spec' in document and 'replicas' in document['spec']:
            #Replicas 1 o 0 (si hay que encender o apagar)
            if estado == "apagar":
                document['spec']['replicas'] = 0
            elif estado == "encender":
                document['spec']['replicas'] = 1

# Guardar los cambios en el archivo YAML
with open(filename, 'w') as file:
    yaml.dump_all(yaml_content, file, default_flow_style=False)

# Aplicamos los cambios al pod
comando_rep = f"kubectl apply -f {filename}"
output = subprocess.run(comando_rep, shell=True, capture_output=True, text=True)

#comando_pod = "kubectl get pods | grep ^"+serv+"- | awk '{print $1}'"
comando_pod = "kubectl get pods | grep ^"+serv+"- | cut -d' ' -f1"
output_pod = subprocess.run(comando_pod, shell=True, capture_output=True, text=True)
#Devolvemos el nombre del pod nuevo
print(output_pod.stdout[0:-1])
