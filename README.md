# 🚗 XONICAR - Taller Manager

**Desarrollado por:** Darian Alberto Camacho Salas

---

## #Somos XONIDU

---
## 🎯 Objetivo

Plataforma web para gestión integral de talleres mecánicos con Flask. Permite a super administradores gestionar múltiples talleres y a administradores controlar vehículos, trabajos y fotografías.

---

## 📋 Características

### 👑 Super Administrador
- Crear y gestionar empresas/talleres
- Crear administradores por empresa
- Activar/desactivar empresas

### 🔧 Administrador de Empresa
- Registrar vehículos con datos del cliente
- Números de orden automáticos (ORDEN-YYYYMMDD-XXXX)
- Estados: pendiente, en proceso, terminado
- Subir fotos por etapa (llegada, proceso, terminado)
- Buscar por placa, cliente o número de orden

---

## 📁 Estructura

```
xonicar/
├── README.md          # Documentación
├── start.py           # Código principal
└── templates/         # Plantillas HTML
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

---

## 📦 Instalación

### Arch Linux
```bash
sudo pacman -Syu python-pip
pip install Flask --break-system-packages
mkdir -p static/fotos data
```

### Ubuntu / Debian
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install Flask --break-system-packages
mkdir -p static/fotos data
```

### Windows
```bash
pip install Flask
mkdir static\fotos data
```

---

## 🚀 Ejecución

```bash
python start.py
```

Accede: `http://localhost:5000` (PC) o `http://TU-IP:5000` (móvil)

---

## 👑 Credenciales por Defecto

| Usuario | Contraseña | Rol |
|---------|------------|-----|
| xonicar123 | xonicar123 | super_admin |

---

## 📝 Formatos Soportados

**Imágenes:** JPG, JPEG, PNG, GIF

---

## 🛠️ Solución de Problemas

- **Puerto ocupado:** Cambia el puerto en `start.py`
- **No se guardan fotos:** Verifica permisos en `static/fotos/`
- **Móvil no conecta:** Verifica firewall y IP

---

## 👨‍💻 Desarrollador

**Darian Alberto Camacho Salas**

---

## 📞 Contacto XONIDU

- 📸 Instagram: @xonidu
- 📘 Facebook: xonidu
- 📧 Email: xonidu@gmail.com

---

**XONICAR v1.0** • Taller Manager • by XONIDU
