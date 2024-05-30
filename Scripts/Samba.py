import subprocess
import sys


argumentos = len(sys.argv)

if argumentos != 3:
    print("Argumentos incorrectos")
    sys.exit(1)
else:
    print("Argumentos Correctos")

user = sys.argv[1]
contra = sys.argv[2]

comando_samba = f"""echo "Super3" | ssh -tt samba@192.168.10.40 '/scripts/crear.sh {user} {contra}'"""
output = subprocess.run(comando_samba, shell=True, capture_output=True, text=True)
