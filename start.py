#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
XONICAR 2026 - Lanzador Universal del Taller Manager
Este script ejecuta xonicar.py y verifica dependencias
Desarrollado por: Darian Alberto Camacho Salas
#Somos: XONIDU
"""

import subprocess
import sys
import os
import platform
import shutil
import importlib.util

# Colores para terminal
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    
    @staticmethod
    def supports_color():
        """Verifica si la terminal soporta colores"""
        if platform.system() == 'Windows':
            try:
                import ctypes
                kernel32 = ctypes.windll.kernel32
                return kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)
            except:
                return False
        return True

# Desactivar colores si no hay soporte
if not Colors.supports_color():
    for attr in dir(Colors):
        if not attr.startswith('_') and attr != 'supports_color':
            setattr(Colors, attr, '')

def get_system():
    """Detecta el sistema operativo"""
    return platform.system().lower()

def get_linux_distro():
    """Detecta la distribucion de Linux"""
    if get_system() != 'linux':
        return None
    
    try:
        if os.path.exists('/etc/os-release'):
            with open('/etc/os-release', 'r') as f:
                content = f.read().lower()
                if 'ubuntu' in content:
                    return 'ubuntu'
                elif 'debian' in content:
                    return 'debian'
                elif 'fedora' in content:
                    return 'fedora'
                elif 'centos' in content:
                    return 'centos'
                elif 'arch' in content:
                    return 'arch'
                elif 'manjaro' in content:
                    return 'manjaro'
                elif 'mint' in content:
                    return 'mint'
        return 'linux-generico'
    except:
        return 'linux-generico'

def get_python_command():
    """Obtiene el comando Python correcto"""
    if get_system() == 'windows':
        return ['python']
    else:
        try:
            subprocess.run(['python3', '--version'], capture_output=True, check=True)
            return ['python3']
        except:
            return ['python']

def print_banner():
    """Muestra el banner de XONICAR"""
    sistema = get_system()
    distro = get_linux_distro()
    
    sistema_texto = {
        'windows': 'WINDOWS',
        'linux': f'LINUX ({distro.upper()})' if distro else 'LINUX',
        'darwin': 'MACOS'
    }.get(sistema, 'DESCONOCIDO')
    
    banner = f"""
{Colors.BLUE}{Colors.BOLD}═══════════════════════════════════════════════════════════
                    XONICAR 2026 v1.0                    
              Sistema de Gestión para Talleres            
              Mecánicos - Multiempresa                
                                                          
              Sistema detectado: {sistema_texto}            
                                                          
              Desarrollado por: Darian Alberto            
              Camacho Salas                               
              #Somos XONIDU
═══════════════════════════════════════════════════════════{Colors.END}
    """
    print(banner)

def check_python():
    """Verifica Python instalado"""
    try:
        cmd = get_python_command() + ['--version']
        subprocess.run(cmd, capture_output=True, check=True)
        return True
    except:
        return False

def check_command(comando):
    """Verifica si un comando existe"""
    return shutil.which(comando) is not None

def check_python_module(module_name):
    """Verifica si un modulo de Python esta instalado"""
    return importlib.util.find_spec(module_name) is not None

def read_requirements():
    """Lee requisitos.txt y devuelve lista de paquetes"""
    req_file = 'requisitos.txt'
    paquetes = []
    if os.path.exists(req_file):
        with open(req_file, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#'):
                    # Extraer solo el nombre del paquete (sin versiones)
                    pkg = line.split('==')[0].split('>=')[0].split('<=')[0].strip()
                    if pkg:
                        paquetes.append(pkg)
    return paquetes

def check_dependencies():
    """Verifica las dependencias de Python necesarias"""
    print(f"\n{Colors.BOLD}Verificando dependencias de Python...{Colors.END}")
    
    # Leer requisitos.txt
    paquetes_requeridos = read_requirements()
    if not paquetes_requeridos:
        # Fallback: Flask como mínimo
        paquetes_requeridos = ['flask']
    
    # Verificar cada paquete
    faltantes = []
    for paquete in paquetes_requeridos:
        # Normalizar nombre de importación (algunos paquetes tienen diferente nombre)
        import_name = paquete.lower().replace('-', '_')
        if import_name == 'flask':
            import_name = 'flask'  # Flask se importa como flask
        # Verificar si está instalado
        if check_python_module(import_name):
            print(f"{Colors.GREEN}  - {paquete}: OK{Colors.END}")
        else:
            print(f"{Colors.YELLOW}  - {paquete}: FALTANTE{Colors.END}")
            faltantes.append(paquete)
    
    # Verificar dependencias del sistema para ciertos paquetes (si es necesario)
    # Flask no requiere dependencias de sistema adicionales, pero podemos dejar esto por si acaso
    # En Linux, a veces se necesita python3-venv, etc. No obligatorio.
    
    return faltantes

def install_dependencies(faltantes):
    """Instala las dependencias faltantes usando pip y requisitos.txt"""
    if not faltantes:
        return True
    
    print(f"\n{Colors.BOLD}Instalando dependencias faltantes...{Colors.END}")
    
    sistema = get_system()
    distro = get_linux_distro()
    
    # Intentar instalar usando requisitos.txt directamente
    req_file = 'requisitos.txt'
    if os.path.exists(req_file):
        print(f"Usando {req_file} para instalar dependencias...")
        # Construir comando de instalacion
        cmd = [sys.executable, '-m', 'pip', 'install', '-r', req_file]
        
        # Agregar opciones segun sistema
        if sistema == 'linux':
            if distro in ['arch', 'manjaro', 'fedora']:
                cmd.append('--break-system-packages')
                print(f"{Colors.YELLOW}Usando --break-system-packages para {distro}{Colors.END}")
            else:
                cmd.append('--user')
        elif sistema == 'darwin':
            cmd.append('--user')
        
        try:
            print(f"Ejecutando: {' '.join(cmd)}")
            subprocess.run(cmd, check=True)
            print(f"{Colors.GREEN}Dependencias instaladas correctamente{Colors.END}")
            return True
        except subprocess.CalledProcessError as e:
            print(f"{Colors.RED}Error instalando dependencias: {e}{Colors.END}")
            print(f"\n{Colors.YELLOW}Intentando metodo alternativo...{Colors.END}")
            # Segundo intento: solo --user
            try:
                cmd2 = [sys.executable, '-m', 'pip', 'install', '--user', '-r', req_file]
                subprocess.run(cmd2, check=True)
                print(f"{Colors.GREEN}Instaladas con --user{Colors.END}")
                return True
            except:
                print(f"{Colors.RED}Fallo la instalacion{Colors.END}")
                print(f"\nInstala manualmente:")
                print(f"  pip install -r {req_file}")
                return False
    else:
        # Fallback: instalar paquetes individuales
        print(f"No se encuentra {req_file}, instalando paquetes individualmente...")
        cmd_base = [sys.executable, '-m', 'pip', 'install']
        if sistema == 'linux':
            if distro in ['arch', 'manjaro', 'fedora']:
                cmd_base.append('--break-system-packages')
            else:
                cmd_base.append('--user')
        elif sistema == 'darwin':
            cmd_base.append('--user')
        
        for paquete in faltantes:
            cmd = cmd_base + [paquete]
            try:
                print(f"Instalando {paquete}...")
                subprocess.run(cmd, check=True)
            except:
                print(f"{Colors.RED}Error instalando {paquete}{Colors.END}")
                return False
        return True

def crear_directorios():
    """Crea los directorios necesarios para la aplicación"""
    print(f"\n{Colors.BOLD}Verificando directorios necesarios...{Colors.END}")
    directorios = ['static/fotos', 'data']
    for d in directorios:
        if not os.path.exists(d):
            os.makedirs(d, exist_ok=True)
            print(f"{Colors.GREEN}  Creado: {d}{Colors.END}")
        else:
            print(f"{Colors.GREEN}  Existente: {d}{Colors.END}")

def mostrar_ayuda():
    """Muestra ayuda de uso"""
    ayuda = f"""
{Colors.BOLD}USO DE XONICAR:{Colors.END}

  python start.py

{Colors.BOLD}DESCRIPCION:{Colors.END}

  XONICAR es un sistema web para gestionar talleres mecánicos.
  Permite a super administradores manejar múltiples empresas y
  a administradores de taller controlar vehículos, trabajos y fotos.

{Colors.BOLD}ACCESO:{Colors.END}

  Después de iniciar, abre tu navegador en:
    http://localhost:5000
    (o http://TU-IP:5000 desde otros dispositivos)

{Colors.BOLD}CREDENCIALES POR DEFECTO:{Colors.END}

  Usuario: xonicar123
  Contraseña: xonicar123
  Rol: super_admin

{Colors.BOLD}ADVERTENCIA:{Colors.END}

  Este programa es para uso legítimo en talleres mecánicos.
  No lo uses para actividades fraudulentas.

{Colors.BOLD}CONTROLES:{Colors.END}

  - Para detener el servidor: Ctrl+C en la terminal
    """
    print(ayuda)

def verificar_importaciones():
    """Verifica que Flask pueda importarse"""
    print(f"\n{Colors.BOLD}Verificando importaciones...{Colors.END}")
    
    try:
        __import__('flask')
        print(f"{Colors.GREEN}  - Flask: OK{Colors.END}")
        return True
    except ImportError:
        print(f"{Colors.RED}  - Flask: FALLO{Colors.END}")
        return False

def crear_accesos_directos():
    """Crea accesos directos para cada sistema"""
    sistema = get_system()
    
    if sistema == 'windows':
        # Crear .bat para Windows
        with open('INICIAR_XONICAR.bat', 'w') as f:
            f.write("""@echo off
title XONICAR 2026 - Taller Manager
color 1F
echo ========================================
echo      XONICAR 2026 - Taller Manager
echo      Desarrollado por Darian Alberto
echo ========================================
echo.
python start.py
pause
""")
        print(f"{Colors.GREEN}Creado INICIAR_XONICAR.bat - Haz doble clic para ejecutar{Colors.END}")
    
    elif sistema == 'linux':
        # Crear .sh para Linux
        with open('INICIAR_XONICAR.sh', 'w') as f:
            f.write("""#!/bin/bash
echo "========================================"
echo "      XONICAR 2026 - Taller Manager"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
read -p "Presiona Enter para salir"
""")
        os.chmod('INICIAR_XONICAR.sh', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONICAR.sh - Ejecuta con: ./INICIAR_XONICAR.sh{Colors.END}")
    
    elif sistema == 'darwin':
        # Crear .command para Mac
        with open('INICIAR_XONICAR.command', 'w') as f:
            f.write("""#!/bin/bash
cd "$(dirname "$0")"
echo "========================================"
echo "      XONICAR 2026 - Taller Manager"
echo "      Desarrollado por Darian Alberto"
echo "========================================"
echo ""
python3 start.py
""")
        os.chmod('INICIAR_XONICAR.command', 0o755)
        print(f"{Colors.GREEN}Creado INICIAR_XONICAR.command - Haz doble clic para ejecutar{Colors.END}")

def main():
    """Funcion principal"""
    # Limpiar pantalla
    if get_system() == 'windows':
        os.system('cls')
    else:
        os.system('clear')
    
    # Mostrar banner
    print_banner()
    
    # Verificar si hay argumentos de ayuda
    if len(sys.argv) > 1 and sys.argv[1] in ['-h', '--help', '/?']:
        mostrar_ayuda()
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar Python
    if not check_python():
        print(f"\n{Colors.RED}Error: Python no esta instalado{Colors.END}")
        print("Instala Python desde: https://www.python.org/downloads/")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    python_version = subprocess.run(get_python_command() + ['--version'], 
                                   capture_output=True, text=True).stdout.strip()
    print(f"{Colors.BOLD}Python:{Colors.END} {python_version}")
    print(f"{Colors.BOLD}Directorio:{Colors.END} {os.path.dirname(os.path.abspath(__file__))}")
    
    # Crear directorios necesarios
    crear_directorios()
    
    # Verificar dependencias
    faltantes = check_dependencies()
    
    if faltantes:
        print(f"\n{Colors.YELLOW}Faltan dependencias: {', '.join(faltantes)}{Colors.END}")
        respuesta = input("Instalar automaticamente? (s/n): ")
        
        if respuesta.lower() == 's':
            install_dependencies(faltantes)
        else:
            print(f"\nPuedes instalarlas manualmente con:")
            print(f"  pip install -r requisitos.txt")
    
    # Verificar que existe xonicar.py
    if not os.path.exists('xonicar.py'):
        print(f"\n{Colors.RED}Error: No se encuentra xonicar.py{Colors.END}")
        print("Asegurate de que xonicar.py esta en el mismo directorio")
        print("\nPuedes descargarlo desde:")
        print("  https://github.com/XONIDU/xonicar")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    # Verificar que Flask puede importarse
    print(f"\n{Colors.BOLD}Verificando que todo funcione...{Colors.END}")
    if not verificar_importaciones():
        print(f"\n{Colors.RED}Error: No se puede importar Flask{Colors.END}")
        print("El programa no puede continuar sin esta dependencia")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
        return
    
    print(f"\n{Colors.BOLD}Iniciando XONICAR...{Colors.END}")
    print(f"{Colors.BOLD}Para detener el servidor:{Colors.END} Ctrl+C")
    print("-" * 60)
    
    # EJECUTAR xonicar.py - LA APLICACIÓN PRINCIPAL
    try:
        python_cmd = get_python_command()
        cmd = python_cmd + ['xonicar.py']
        print(f"Ejecutando: {' '.join(cmd)}")
        print("-" * 60)
        
        # Ejecutar xonicar.py
        resultado = subprocess.run(cmd)
        
        if resultado.returncode != 0:
            print(f"\n{Colors.RED}Error: xonicar.py termino con codigo {resultado.returncode}{Colors.END}")
            
    except FileNotFoundError:
        print(f"\n{Colors.RED}Error: No se encuentra xonicar.py{Colors.END}")
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Servidor detenido por el usuario{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error ejecutando xonicar.py: {e}{Colors.END}")
    
    print(f"\n{Colors.BLUE}Gracias por usar XONICAR 2026{Colors.END}")
    print(f"{Colors.BLUE}Desarrollado por Darian Alberto Camacho Salas{Colors.END}")
    print(f"{Colors.BLUE}#Somos XONIDU{Colors.END}")
    
    # Pausa al final (excepto en Windows que ya tiene pausa por el .bat)
    if get_system() != 'windows':
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")

if __name__ == '__main__':
    try:
        # Crear accesos directos
        crear_accesos_directos()
        
        # Ejecutar programa principal
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Saliendo...{Colors.END}")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {e}{Colors.END}")
        input(f"\n{Colors.YELLOW}Presiona Enter para salir...{Colors.END}")
