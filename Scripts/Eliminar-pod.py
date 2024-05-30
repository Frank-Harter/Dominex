import subprocess
import sys
import pymysql

server_name = sys.argv[1]
nombre_usu = sys.argv[2]
Eli_service = 'kubectl delete service ' + server_name
subprocess.run(Eli_service, shell=True)

Eli_deployment = 'kubectl delete deployment ' + server_name
subprocess.run(Eli_deployment, shell=True)

Eli_pvc = 'kubectl delete pvc ' + server_name
subprocess.run(Eli_pvc, shell=True)

Eli_pv = 'kubectl delete pv ' + server_name
subprocess.run(Eli_pv, shell=True)



try:
    conn = pymysql.connect(host='192.168.10.90', port=3307, user='admin', password='Super3ies1234.', db='FDominex', charset='utf8mb4')

    #conn = pymysql.connect(host='192.168.10.200', user='root', password='Super3ies1234.', db='FDominex', charset='utf8mb4')
    with conn.cursor() as cursor:
        # Realizar una consulta
        sele = f"SELECT puerto FROM FDominex.servidores WHERE dominio = '{server_name}';"
        cursor.execute(sele)
        result = cursor.fetchone()
        puerto = result[0]
        delete = f"""DELETE FROM FDominex.servidores WHERE dominio='{server_name}';"""
        cursor.execute(delete)
        conn.commit()
        comando_pfsense = f"ssh -i /home/master/.ssh/id_rsa_new admin@192.168.10.1 'python3.11 /eliminar.py {puerto}'"
        output = subprocess.run(comando_pfsense, shell=True, capture_output=True, text=True)
        comando_samba = f"rm -r /mnt/samba/clientes/.{nombre_usu}/{server_name}"
        output = subprocess.run(comando_samba, shell=True, capture_output=True, text=True)
        comando_dns = f"ssh master@192.168.10.60 -i /home/master/.ssh/dnss 'python3 /etc/bind/zonas/delete-dns.py {server_name}'"
        output = subprocess.run(comando_dns, shell=True, capture_output=True, text=True)


finally:
    conn.close()

