#! /usr/bin/python3
import getpass
import subprocess
import re

#Devuelve SO del host
def CheckOS():
    p = subprocess.run(["cat", "/etc/os-release"], capture_output=True)
    extractSysVars = p.stdout
    '''
    searchOS = re.findall('(\w+)\s*=\s*\"([\w%-]+)"', str(extractSysVars))
    for element in searchOS:
        if element[0].lower() =="NAME":
            foundOS = element[1]
            break
    '''
    foundOS = re.findall('ID=(\w+)', str(extractSysVars))
    
    return foundOS[0]

#Crea el entorno de python especificado. Devuelve None.
def CreateEnv(foundOS,passUser,envName ="MainEnv"):
    relationEnv = {"fedora":["dnf", ""], "ubuntu":["apt-get","3"],"raspbian":["apt-get","3"]}
    commonParams = {"text":True, "check":True, "stdout":subprocess.DEVNULL}
    try:
        print("Actualizando repositorios...")
        p1 = subprocess.run(["sudo", "-S", f"{relationEnv[foundOS][0]}","update"], input=passUser, **commonParams)
        print("OK\n" if p1.returncode==0 else "Error")

        print("Verificando/Instalando paquete de entorno...")
        p2 = subprocess.run(["sudo", "-S", f"{relationEnv[foundOS][0]}", "install", "-y", f"python{relationEnv[foundOS][1]}-virtualenv"], input=passUser, **commonParams)
        print("OK\n" if p2.returncode==0 else "Error")
        
        print("Creando entorno...")
        p3 = subprocess.run([f"python{relationEnv[foundOS][1]}", "-m", "venv", f"{envName}"],**commonParams)
        print("OK\n" if p3.returncode==0 else "Error")
        
        print("Activando entorno e instalando dependencias...")
        p4 = subprocess.run(f"source {envName}/bin/activate && pip{relationEnv[foundOS][1]} install -r requirements.txt", shell=True, executable="/bin/bash",**commonParams)
        print("OK\n" if p4.returncode==0 else "Error")

        print("¡Entorno creado! Verifique que todo esté en orden")

    except subprocess.CalledProcessError:
        raise Exception("Contraseña root mal introducida")


if __name__ == "__main__":
    #envName = input("Introduce nombre del entorno a crear: ")
    passUser = getpass.getpass("Introduce tu contraseña root: ")
    foundOS = CheckOS()
    envManaged = CreateEnv(foundOS.lower(), passUser)
