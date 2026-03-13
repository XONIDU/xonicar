# 🚗 XONICAR - Taller Manager

**Advertencia:** Este sistema está diseñado para uso legítimo en talleres mecánicos. El autor no se hace responsable del uso dado.

## 🎯 ¿Qué es XONICAR?

Plataforma web con Flask para gestión integral de talleres mecánicos. Permite:

- **Multi-tenant**: Gestionar múltiples talleres
- **Control de vehículos**: Registro y seguimiento por estados
- **Gestión fotográfica**: Imágenes por etapa (llegada, proceso, terminado)
- **Sistema de roles**: Super admin y admin de empresa

## 📥 Instalación

```bash
git clone https://github.com/XONIDU/xonicar.git
cd xonicar
```

### Dependencias:

**Arch Linux**
```bash
sudo pacman -Syu python-pip
pip install -r requisitos.txt --break-system-packages
mkdir -p static/fotos data
```

**Ubuntu/Debian**
```bash
sudo apt update
sudo apt install -y python3 python3-pip
pip3 install -r requisitos.txt --break-system-packages
mkdir -p static/fotos data
```

**Windows**
```bash
pip install -r requisitos.txt
mkdir static\fotos data
```

## ⚙️ Uso

```bash
python start.py
```
Accede: `http://localhost:5000`

### Credenciales por defecto:
| Usuario | Contraseña | Rol |
|---------|------------|-----|
| xonicar123 | xonicar123 | super_admin |

## 👑 Funcionalidades

**Super Admin**
- Crear/gestionar empresas
- Crear admins por empresa
- Activar/desactivar empresas

**Admin de Empresa**
- Registrar vehículos con datos del cliente
- Números automáticos: ORDEN-YYYYMMDD-XXXX
- Estados: pendiente, proceso, terminado
- Subir fotos por etapa
- Buscar por placa, cliente u orden

## 📁 Estructura

```
xonicar/
├── start.py
├── requisitos.txt
├── data/          # JSONs
├── static/fotos/  # Imágenes
└── templates/     # HTMLs
```

## 📝 Formatos

Imágenes: JPG, JPEG, PNG, GIF

## ✉️ Contacto

- **Creador**: Darian Alberto Camacho Salas
- **Email**: xonidu@gmail.com
- **IG**: @xonidu | **FB**: xonidu
- **#Somos XONIDU**

---

**XONICAR v4.2.0** • by XONIDU
**Creador:** Darian Alberto Camacho Salas
