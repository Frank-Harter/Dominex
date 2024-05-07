import subprocess
import sys

server_name = sys.argv[1]

Eli_service = 'kubectl delete service ' + server_name
subprocess.run(Eli_service, shell=True)

Eli_deployment = 'kubectl delete deployment ' + server_name
subprocess.run(Eli_deployment, shell=True)

Eli_pvc = 'kubectl delete pvc ' + server_name
subprocess.run(Eli_pvc, shell=True)

Eli_pv = 'kubectl delete pv ' + server_name
subprocess.run(Eli_pv, shell=True)



