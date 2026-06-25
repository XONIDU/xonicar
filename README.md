# 🚗 XONICAR - Taller Manager

**Advertencia:** Este sistema está diseñado para uso legítimo en talleres mecánicos. No debe utilizarse para actividades fraudulentas o malintencionadas. El autor no se hace responsable del uso indebido de esta aplicación.

## 🎯 ¿Qué es XONICAR?

**XONICAR** es una plataforma web desarrollada con Flask para la gestión integral de talleres mecánicos. Permite:

- **Multi‑tenant:** Gestionar múltiples empresas/talleres desde una sola instancia.
- **Control de vehículos:** Registro completo con datos del cliente y seguimiento por estados (pendiente, en proceso, terminado).
- **Gestión fotográfica:** Subida de imágenes por etapa (llegada, proceso, terminado).
- **Sistema de roles:** Super administradores y administradores de empresa con diferentes permisos.

## 📥 Instalación

Clona el repositorio desde GitHub:

```bash
git clone https://github.com/XONIDU/xonicar.git
cd xonicar
```

## ✅ Requisitos

- Python 3.8+ instalado.
- Dependencias Python listadas en `requisitos.txt`.
- Permisos de escritura en el directorio para almacenar datos e imágenes.

### Dependencias del sistema por plataforma:

#### 🐧 Arch Linux / Manjaro

```bash
sudo pacman -Syu python-pip
pip install -r requisitos.txt --break-system-packages
mkdir -p static/fotos data
```

#### 🐧 Ubuntu / Debian / Linux Mint

```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requisitos.txt --break-system-packages
mkdir -p static/fotos data
```

#### 🐧 Fedora

```bash
sudo dnf install python3 python3-pip
pip3 install -r requisitos.txt --break-system-packages
mkdir -p static/fotos data
```

---

### Opción 2 – Comando `xoninstall` (recomendado para futuras herramientas XONI)

Agrega la siguiente función a tu `~/.bashrc` con un solo comando:

```bash
echo 'xoninstall() { if [ -z "$1" ]; then echo "Uso: xoninstall <repo>"; echo "Ej: xoninstall xoniran"; else git clone "https://github.com/XONIDU/$1.git"; fi; }' >> ~/.bashrc && source ~/.bashrc && echo "✅ Listo. Usa: xoninstall xonicli"
```

Luego simplemente escribe:

```bash
xoninstall xonicar
cd xonicar
pip install -r requisitos.txt
python start.py
```

> **Nota:** Esta función te servirá para instalar cualquier otra herramienta futura de XONIDU (por ejemplo `xoninstall xonicli`).

---

#### 🪟 Windows

```bash
pip install -r requisitos.txt
mkdir static\fotos data
```

#### 🍎 macOS

```bash
pip3 install -r requisitos.txt --user
mkdir -p static/fotos data
```

## ⚙️ Uso

### En Windows (recomendado)

Ejecuta directamente el archivo **XONICAR.bat** que ya incluye permisos de administrador:

```bash
XONICAR.bat
```

Este archivo:

- Solicita automáticamente permisos de administrador (UAC).
- Verifica e instala dependencias si es necesario.
- Inicia el servidor en `http://localhost:5000`.
- Muestra un mensaje claro de que está funcionando.

### En Linux / macOS

Ejecuta el lanzador:

```bash
python start.py
```

El script verificará e instalará las dependencias necesarias (con `--break-system-packages` en las distribuciones que lo requieran) y luego arrancará automáticamente la aplicación principal `xonicar.py`.

Accede a la plataforma:

- **Local:** `http://localhost:5000`
- **Desde otros dispositivos:** `http://TU-IP:5000`

### Credenciales por defecto

| Usuario      | Contraseña   | Rol          |
|--------------|--------------|--------------|
| xonicar123   | xonicar123   | super_admin  |

## 👑 Funcionalidades por Rol

### Super Administrador
- ✅ Crear y gestionar empresas/talleres.
- ✅ Crear administradores por empresa.
- ✅ Activar/desactivar empresas.

### Administrador de Empresa
- ✅ Registrar vehículos con datos del cliente.
- ✅ Números de orden automáticos (`ORDEN-YYYYMMDD-XXXX`).
- ✅ Estados: pendiente, en proceso, terminado.
- ✅ Subir fotos por etapa (llegada, proceso, terminado).
- ✅ Buscar por placa, cliente o número de orden.

## 📁 Estructura del Proyecto

```
xonicar/
├── README.md                    # Documentación
├── XONICAR.bat                   # Lanzador para Windows (con UAC)
├── start.py                      # Lanzador (verifica dependencias y ejecuta)
├── xonicar.py                    # Aplicación principal Flask
├── requisitos.txt                # Dependencias Python
├── data/                         # Almacenamiento JSON
│   ├── empresas.json
│   ├── usuarios.json
│   └── vehiculos.json
├── static/
│   └── fotos/                    # Imágenes subidas
└── templates/                    # Plantillas HTML
    ├── login.html
    ├── dashboard_super_admin.html
    ├── dashboard_admin_empresa.html
    ├── nueva_empresa.html
    ├── nuevo_admin_empresa.html
    ├── lista_vehiculos.html
    ├── nuevo_vehiculo.html
    ├── ver_vehiculo.html
    └── subir_fotos.html
```

## 📝 Formatos Soportados

- **Imágenes:** JPG, JPEG, PNG, GIF

## 🔒 Consideraciones de seguridad

- La aplicación almacena datos localmente en archivos JSON.
- Las contraseñas se guardan en texto plano (mejorable con hashing en futuras versiones).
- No expongas esta aplicación directamente a internet sin medidas de seguridad adicionales (como un proxy inverso con HTTPS y autenticación robusta).
- Realiza copias de seguridad periódicas de los directorios `data/` y `static/fotos/`.

## 🐛 Problemas comunes

- **“Puerto ocupado”**: Cambia el puerto en `xonicar.py` (línea `app.run(port=5000)`).
- **“No se guardan fotos”**: Verifica permisos de escritura en `static/fotos/`.
- **“Móvil no conecta”**: Comprueba el firewall y que uses la IP correcta de la máquina anfitriona.
- **“Error al cargar imágenes”**: Verifica que el formato sea soportado (JPG, JPEG, PNG, GIF).
- **“Error de permisos en Windows”**: Ejecuta `XONICAR.bat` como administrador (clic derecho → "Ejecutar como administrador").

## 📦 Archivos incluidos

- `XONICAR.bat` — Lanzador para Windows con solicitud automática de permisos de administrador.
- `start.py` — Lanzador universal (Linux/macOS/Windows) que verifica dependencias.
- `xonicar.py` — Aplicación principal Flask.
- `requisitos.txt` — Dependencias Python.
- `README.md` — Documentación completa.

## ✉️ Contacto y Créditos

- **Proyecto:** XONIDU
- **Creador:** Darian Alberto Camacho Salas
- **Email:** xonidu@gmail.com
- **Redes sociales:** 
  - 📸 Instagram: [@xonidu](https://instagram.com/xonidu)
  - 📘 Facebook: [xonidu](https://facebook.com/xonidu)
- **#Somos XONIDU**

