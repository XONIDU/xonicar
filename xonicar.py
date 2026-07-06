from flask import Flask, render_template, request, redirect, url_for, flash, session
import os
import csv
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from datetime import datetime
from functools import wraps
import secrets
import string

app = Flask(__name__)
app.secret_key = "clave_super_secreta_xonicar123"

# Configuración básica
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'fotos')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Archivos CSV
DATA_FOLDER = os.path.join(BASE_DIR, 'data')
os.makedirs(DATA_FOLDER, exist_ok=True)

USUARIOS_CSV = os.path.join(DATA_FOLDER, 'usuarios.csv')
EMPRESAS_CSV = os.path.join(DATA_FOLDER, 'empresas.csv')
VEHICULOS_CSV = os.path.join(DATA_FOLDER, 'vehiculos.csv')
TRABAJOS_CSV = os.path.join(DATA_FOLDER, 'trabajos.csv')
FOTOS_CSV = os.path.join(DATA_FOLDER, 'fotos.csv')

# =============================================
# FUNCIONES AUXILIARES
# =============================================

def leer_csv(archivo):
    if not os.path.exists(archivo):
        return []
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return list(csv.DictReader(f))
    except:
        return []

def escribir_csv(archivo, datos, campos):
    with open(archivo, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        if datos:
            writer.writerows(datos)

def generar_id():
    return ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(8))

def generar_numero_orden():
    fecha = datetime.now().strftime('%Y%m%d')
    trabajos = leer_csv(TRABAJOS_CSV)
    ordenes_hoy = [t['numero_orden'] for t in trabajos if fecha in t.get('numero_orden', '')]
    
    if ordenes_hoy:
        try:
            ultimo = max([int(o.split('-')[-1]) for o in ordenes_hoy])
            nuevo = ultimo + 1
        except:
            nuevo = 1
    else:
        nuevo = 1
    
    return f"ORDEN-{fecha}-{nuevo:04d}"

def inicializar_sistema():
    # Crear super admin si no existe
    if not os.path.exists(USUARIOS_CSV):
        super_admin = {
            'username': 'xonicar123',
            'password': 'xonicar123',
            'nombre': 'Super Administrador',
            'email': 'admin@taller.com',
            'telefono': '5550000001',
            'rol': 'super_admin',
            'empresa_id': '',
            'creado_por': 'sistema',
            'activo': '1'
        }
        
        with open(USUARIOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['username', 'password', 'nombre', 'email', 'telefono', 
                           'rol', 'empresa_id', 'creado_por', 'activo'])
            writer.writerow([super_admin['username'], super_admin['password'], 
                           super_admin['nombre'], super_admin['email'], 
                           super_admin['telefono'], super_admin['rol'], 
                           super_admin['empresa_id'], super_admin['creado_por'], 
                           super_admin['activo']])
    
    # Empresas
    if not os.path.exists(EMPRESAS_CSV):
        with open(EMPRESAS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'nombre', 'direccion', 'telefono', 'email', 
                           'fecha_registro', 'creado_por', 'activo'])
    
    # Vehículos
    if not os.path.exists(VEHICULOS_CSV):
        with open(VEHICULOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'empresa_id', 'cliente_nombre', 'cliente_email', 
                           'cliente_telefono', 'marca', 'modelo', 'año', 'color', 
                           'placa', 'vin', 'fecha_ingreso', 'estado', 'numero_orden'])
    
    # Trabajos
    if not os.path.exists(TRABAJOS_CSV):
        with open(TRABAJOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'vehiculo_id', 'empresa_id', 'numero_orden', 
                           'estado', 'descripcion', 'observaciones', 'costo_estimado', 
                           'fecha_inicio', 'ultima_actualizacion'])
    
    # Fotos
    if not os.path.exists(FOTOS_CSV):
        with open(FOTOS_CSV, 'w', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            writer.writerow(['id', 'trabajo_id', 'empresa_id', 'tipo_foto', 
                           'ruta_foto', 'descripcion', 'fecha_subida', 'correo_enviado'])

# =============================================
# DECORADORES DE AUTENTICACIÓN
# =============================================

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def super_admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('rol') != 'super_admin':
            flash('Acceso denegado. Requiere permisos de super administrador.')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

def admin_empresa_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session or session.get('rol') != 'admin_empresa':
            flash('Acceso denegado. Requiere permisos de administrador.')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

# =============================================
# RUTAS DE LA APLICACIÓN
# =============================================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        usuarios = leer_csv(USUARIOS_CSV)
        usuario = next((u for u in usuarios if u['username'] == username and 
                       u['password'] == password and u['activo'] == '1'), None)
        
        if usuario:
            session['username'] = username
            session['nombre'] = usuario['nombre']
            session['rol'] = usuario['rol']
            session['empresa_id'] = usuario['empresa_id']
            
            flash(f'✅ ¡Bienvenido {usuario["nombre"]}!')
            return redirect(url_for('dashboard'))
        else:
            flash('❌ Usuario o contraseña incorrectos')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('🔒 Sesión cerrada correctamente')
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    rol = session.get('rol')
    
    if rol == 'super_admin':
        return redirect(url_for('dashboard_super_admin'))
    elif rol == 'admin_empresa':
        return redirect(url_for('dashboard_admin_empresa'))
    else:
        flash('⚠️ Rol no reconocido')
        return redirect(url_for('logout'))

# =============================================
# RUTAS SUPER ADMIN
# =============================================

@app.route('/dashboard/super-admin')
@super_admin_required
def dashboard_super_admin():
    empresas = leer_csv(EMPRESAS_CSV)
    usuarios = leer_csv(USUARIOS_CSV)
    
    # Filtrar solo administradores de empresa
    admins_empresa = [u for u in usuarios if u['rol'] == 'admin_empresa']
    
    # Obtener estadísticas
    stats = {
        'total_empresas': len(empresas),
        'total_admins': len(admins_empresa),
        'empresas_activas': len([e for e in empresas if e.get('activo') == '1']),
        'empresas_inactivas': len([e for e in empresas if e.get('activo') == '0'])
    }
    
    return render_template('dashboard_super_admin.html', 
                         empresas=empresas, 
                         admins=admins_empresa, 
                         stats=stats)

@app.route('/super-admin/empresas/nueva', methods=['GET', 'POST'])
@super_admin_required
def nueva_empresa():
    if request.method == 'POST':
        nombre = request.form['nombre']
        direccion = request.form.get('direccion', '')
        telefono = request.form['telefono']
        email = request.form['email']
        
        # Crear empresa
        empresa_id = generar_id()
        nueva_empresa = {
            'id': empresa_id,
            'nombre': nombre,
            'direccion': direccion,
            'telefono': telefono,
            'email': email,
            'fecha_registro': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'creado_por': session['username'],
            'activo': '1'
        }
        
        empresas = leer_csv(EMPRESAS_CSV)
        empresas.append(nueva_empresa)
        escribir_csv(EMPRESAS_CSV, empresas, 
                   ['id', 'nombre', 'direccion', 'telefono', 'email', 
                    'fecha_registro', 'creado_por', 'activo'])
        
        flash(f'✅ Empresa "{nombre}" creada exitosamente')
        return redirect(url_for('dashboard_super_admin'))
    
    return render_template('nueva_empresa.html')

@app.route('/super-admin/usuarios/nuevo', methods=['GET', 'POST'])
@super_admin_required
def nuevo_admin_empresa():
    empresas = leer_csv(EMPRESAS_CSV)
    
    if request.method == 'POST':
        empresa_id = request.form['empresa_id']
        username = request.form['username']
        password = request.form['password']
        nombre = request.form['nombre']
        email = request.form['email']
        telefono = request.form.get('telefono', '')
        
        # Verificar si el usuario ya existe
        usuarios = leer_csv(USUARIOS_CSV)
        if any(u['username'] == username for u in usuarios):
            flash('❌ El nombre de usuario ya existe')
            return redirect(url_for('nuevo_admin_empresa'))
        
        # Crear usuario admin
        nuevo_usuario = {
            'username': username,
            'password': password,
            'nombre': nombre,
            'email': email,
            'telefono': telefono,
            'rol': 'admin_empresa',
            'empresa_id': empresa_id,
            'creado_por': session['username'],
            'activo': '1'
        }
        
        usuarios.append(nuevo_usuario)
        escribir_csv(USUARIOS_CSV, usuarios, 
                   ['username', 'password', 'nombre', 'email', 'telefono', 
                    'rol', 'empresa_id', 'creado_por', 'activo'])
        
        flash(f'✅ Administrador "{nombre}" creado exitosamente')
        return redirect(url_for('dashboard_super_admin'))
    
    return render_template('nuevo_admin_empresa.html', empresas=empresas)

@app.route('/super-admin/empresa/<empresa_id>/toggle')
@super_admin_required
def toggle_empresa(empresa_id):
    empresas = leer_csv(EMPRESAS_CSV)
    
    for empresa in empresas:
        if empresa['id'] == empresa_id:
            empresa['activo'] = '0' if empresa.get('activo') == '1' else '1'
            estado = "activada" if empresa['activo'] == '1' else "desactivada"
            break
    
    escribir_csv(EMPRESAS_CSV, empresas, 
               ['id', 'nombre', 'direccion', 'telefono', 'email', 
                'fecha_registro', 'creado_por', 'activo'])
    
    flash(f'✅ Empresa {estado} exitosamente')
    return redirect(url_for('dashboard_super_admin'))

# =============================================
# RUTAS ADMIN EMPRESA
# =============================================

@app.route('/dashboard/admin-empresa')
@admin_empresa_required
def dashboard_admin_empresa():
    empresa_id = session.get('empresa_id')
    
    vehiculos = leer_csv(VEHICULOS_CSV)
    trabajos = leer_csv(TRABAJOS_CSV)
    empresas = leer_csv(EMPRESAS_CSV)
    
    # Filtrar por empresa
    vehiculos_empresa = [v for v in vehiculos if v['empresa_id'] == empresa_id]
    trabajos_empresa = [t for t in trabajos if t['empresa_id'] == empresa_id]
    
    # Obtener info de la empresa
    empresa_info = next((e for e in empresas if e['id'] == empresa_id), None)
    
    # Estadísticas
    stats = {
        'total_vehiculos': len(vehiculos_empresa),
        'trabajos_pendientes': len([t for t in trabajos_empresa if t['estado'] == 'pendiente']),
        'trabajos_proceso': len([t for t in trabajos_empresa if t['estado'] == 'en_proceso']),
        'trabajos_terminados': len([t for t in trabajos_empresa if t['estado'] == 'terminado'])
    }
    
    # Obtener últimos 10 vehículos
    vehiculos_recientes = sorted(vehiculos_empresa, 
                                key=lambda x: x.get('fecha_ingreso', ''), 
                                reverse=True)[:10]
    
    # Añadir ID del trabajo a cada vehículo
    for vehiculo in vehiculos_recientes:
        trabajo = next((t for t in trabajos_empresa if t['vehiculo_id'] == vehiculo['id']), None)
        if trabajo:
            vehiculo['trabajo_id'] = trabajo['id']
    
    return render_template('dashboard_admin_empresa.html', 
                         vehiculos=vehiculos_recientes, 
                         stats=stats,
                         empresa_info=empresa_info)

@app.route('/admin/vehiculos')
@admin_empresa_required
def lista_vehiculos():
    empresa_id = session.get('empresa_id')
    
    vehiculos = leer_csv(VEHICULOS_CSV)
    trabajos = leer_csv(TRABAJOS_CSV)
    
    # Filtrar por empresa
    vehiculos_empresa = [v for v in vehiculos if v['empresa_id'] == empresa_id]
    
    # Aplicar filtros
    estado_filter = request.args.get('estado')
    if estado_filter:
        vehiculos_empresa = [v for v in vehiculos_empresa if v['estado'] == estado_filter]
    
    search_filter = request.args.get('search')
    if search_filter:
        search_lower = search_filter.lower()
        vehiculos_empresa = [v for v in vehiculos_empresa if 
                            search_lower in v['cliente_nombre'].lower() or 
                            search_lower in v['placa'].lower() or 
                            search_lower in v['numero_orden'].lower()]
    
    # Añadir ID del trabajo a cada vehículo
    for vehiculo in vehiculos_empresa:
        trabajo = next((t for t in trabajos if t['vehiculo_id'] == vehiculo['id']), None)
        if trabajo:
            vehiculo['trabajo_id'] = trabajo['id']
    
    # Ordenar por fecha de ingreso (más recientes primero)
    vehiculos_empresa = sorted(vehiculos_empresa, 
                              key=lambda x: x.get('fecha_ingreso', ''), 
                              reverse=True)
    
    # Aplicar límite
    limit = int(request.args.get('limit', 10))
    vehiculos_empresa = vehiculos_empresa[:limit]
    
    return render_template('lista_vehiculos.html', 
                         vehiculos=vehiculos_empresa,
                         total_vehiculos=len([v for v in vehiculos if v['empresa_id'] == empresa_id]))

@app.route('/admin/vehiculos/nuevo', methods=['GET', 'POST'])
@admin_empresa_required
def nuevo_vehiculo():
    empresa_id = session.get('empresa_id')
    
    if request.method == 'POST':
        # Datos del cliente
        cliente_nombre = request.form['cliente_nombre']
        cliente_email = request.form.get('cliente_email', '')
        cliente_telefono = request.form['cliente_telefono']
        
        # Datos del vehículo
        marca = request.form['marca']
        modelo = request.form['modelo']
        año = request.form['año']
        color = request.form.get('color', '')
        placa = request.form['placa']
        vin = request.form.get('vin', '')
        
        # Datos del trabajo
        descripcion = request.form['descripcion']
        estado = request.form['estado']
        costo_estimado = request.form.get('costo_estimado', '0')
        
        # Generar IDs y número de orden
        vehiculo_id = generar_id()
        trabajo_id = generar_id()
        numero_orden = generar_numero_orden()
        fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Guardar vehículo
        nuevo_vehiculo = {
            'id': vehiculo_id,
            'empresa_id': empresa_id,
            'cliente_nombre': cliente_nombre,
            'cliente_email': cliente_email,
            'cliente_telefono': cliente_telefono,
            'marca': marca,
            'modelo': modelo,
            'año': año,
            'color': color,
            'placa': placa,
            'vin': vin,
            'fecha_ingreso': fecha_actual,
            'estado': estado,
            'numero_orden': numero_orden
        }
        
        # Guardar trabajo
        nuevo_trabajo = {
            'id': trabajo_id,
            'vehiculo_id': vehiculo_id,
            'empresa_id': empresa_id,
            'numero_orden': numero_orden,
            'estado': estado,
            'descripcion': descripcion,
            'observaciones': '',
            'costo_estimado': costo_estimado,
            'fecha_inicio': fecha_actual,
            'ultima_actualizacion': fecha_actual
        }
        
        # Guardar en CSV
        vehiculos = leer_csv(VEHICULOS_CSV)
        vehiculos.append(nuevo_vehiculo)
        escribir_csv(VEHICULOS_CSV, vehiculos, 
                   ['id', 'empresa_id', 'cliente_nombre', 'cliente_email', 
                    'cliente_telefono', 'marca', 'modelo', 'año', 'color', 
                    'placa', 'vin', 'fecha_ingreso', 'estado', 'numero_orden'])
        
        trabajos = leer_csv(TRABAJOS_CSV)
        trabajos.append(nuevo_trabajo)
        escribir_csv(TRABAJOS_CSV, trabajos, 
                   ['id', 'vehiculo_id', 'empresa_id', 'numero_orden', 
                    'estado', 'descripcion', 'observaciones', 'costo_estimado', 
                    'fecha_inicio', 'ultima_actualizacion'])
        
        flash(f'✅ Vehículo registrado exitosamente. Número de orden: {numero_orden}')
        return redirect(url_for('ver_vehiculo', vehiculo_id=vehiculo_id))
    
    return render_template('nuevo_vehiculo.html')

@app.route('/admin/vehiculo/<vehiculo_id>')
@admin_empresa_required
def ver_vehiculo(vehiculo_id):
    empresa_id = session.get('empresa_id')
    
    vehiculos = leer_csv(VEHICULOS_CSV)
    trabajos = leer_csv(TRABAJOS_CSV)
    fotos = leer_csv(FOTOS_CSV)
    
    vehiculo = next((v for v in vehiculos if v['id'] == vehiculo_id and v['empresa_id'] == empresa_id), None)
    
    if not vehiculo:
        flash('❌ Vehículo no encontrado o no tienes permiso para acceder')
        return redirect(url_for('dashboard_admin_empresa'))
    
    trabajo = next((t for t in trabajos if t['vehiculo_id'] == vehiculo_id), {})
    fotos_vehiculo = [f for f in fotos if f.get('trabajo_id') == trabajo.get('id')]
    
    # Separar fotos por tipo
    fotos_llegada = [f for f in fotos_vehiculo if f.get('tipo_foto') == 'llegada']
    fotos_proceso = [f for f in fotos_vehiculo if f.get('tipo_foto') == 'proceso']
    fotos_terminado = [f for f in fotos_vehiculo if f.get('tipo_foto') == 'terminado']
    
    return render_template('ver_vehiculo.html', 
                         vehiculo=vehiculo, 
                         trabajo=trabajo,
                         fotos_llegada=fotos_llegada,
                         fotos_proceso=fotos_proceso,
                         fotos_terminado=fotos_terminado)

@app.route('/admin/trabajo/<trabajo_id>/subir-fotos', methods=['GET', 'POST'])
@admin_empresa_required
def subir_fotos_trabajo(trabajo_id):
    empresa_id = session.get('empresa_id')
    
    trabajos = leer_csv(TRABAJOS_CSV)
    vehiculos = leer_csv(VEHICULOS_CSV)
    fotos = leer_csv(FOTOS_CSV)
    
    trabajo = next((t for t in trabajos if t['id'] == trabajo_id and t['empresa_id'] == empresa_id), None)
    
    if not trabajo:
        flash('❌ Trabajo no encontrado')
        return redirect(url_for('dashboard_admin_empresa'))
    
    vehiculo = next((v for v in vehiculos if v['id'] == trabajo['vehiculo_id']), None)
    
    if request.method == 'POST':
        tipo_foto = request.form['tipo_foto']
        descripcion = request.form.get('descripcion', '')
        archivos = request.files.getlist('fotos')
        
        fotos_subidas = []
        
        for archivo in archivos:
            if archivo and archivo.filename:
                # Generar nombre único
                extension = os.path.splitext(archivo.filename)[1].lower()
                if extension not in ['.jpg', '.jpeg', '.png', '.gif']:
                    flash(f'❌ Formato no permitido: {extension}')
                    continue
                
                nombre_unico = f"{trabajo_id}_{tipo_foto}_{generar_id()}{extension}"
                ruta_guardado = os.path.join(app.config['UPLOAD_FOLDER'], nombre_unico)
                
                # Guardar archivo
                try:
                    archivo.save(ruta_guardado)
                except Exception as e:
                    flash(f'❌ Error al guardar archivo: {str(e)}')
                    continue
                
                # Registrar en CSV
                nueva_foto = {
                    'id': generar_id(),
                    'trabajo_id': trabajo_id,
                    'empresa_id': empresa_id,
                    'tipo_foto': tipo_foto,
                    'ruta_foto': f'fotos/{nombre_unico}',
                    'descripcion': descripcion,
                    'fecha_subida': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'correo_enviado': '0'
                }
                
                fotos.append(nueva_foto)
                escribir_csv(FOTOS_CSV, fotos, 
                           ['id', 'trabajo_id', 'empresa_id', 'tipo_foto', 
                            'ruta_foto', 'descripcion', 'fecha_subida', 'correo_enviado'])
                
                fotos_subidas.append(nueva_foto)
        
        if fotos_subidas:
            flash(f'✅ {len(fotos_subidas)} fotos subidas exitosamente')
            
            # Actualizar estado del trabajo si es necesario
            if tipo_foto == 'terminado':
                trabajo['estado'] = 'terminado'
                trabajo['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                
                # Actualizar vehículo también
                if vehiculo:
                    vehiculo['estado'] = 'terminado'
                    todos_vehiculos = leer_csv(VEHICULOS_CSV)
                    for v in todos_vehiculos:
                        if v['id'] == vehiculo['id']:
                            v['estado'] = 'terminado'
                            break
                    escribir_csv(VEHICULOS_CSV, todos_vehiculos, 
                               ['id', 'empresa_id', 'cliente_nombre', 'cliente_email', 
                                'cliente_telefono', 'marca', 'modelo', 'año', 'color', 
                                'placa', 'vin', 'fecha_ingreso', 'estado', 'numero_orden'])
                
                escribir_csv(TRABAJOS_CSV, trabajos, 
                           ['id', 'vehiculo_id', 'empresa_id', 'numero_orden', 
                            'estado', 'descripcion', 'observaciones', 'costo_estimado', 
                            'fecha_inicio', 'ultima_actualizacion'])
        
        return redirect(url_for('ver_vehiculo', vehiculo_id=trabajo['vehiculo_id']))
    
    # Obtener fotos existentes para este trabajo
    fotos_existentes = [f for f in fotos if f.get('trabajo_id') == trabajo_id]
    
    return render_template('subir_fotos.html', 
                         trabajo=trabajo, 
                         vehiculo=vehiculo,
                         fotos_existentes=fotos_existentes)

@app.route('/admin/trabajo/<trabajo_id>/actualizar-estado', methods=['POST'])
@admin_empresa_required
def actualizar_estado_trabajo(trabajo_id):
    empresa_id = session.get('empresa_id')
    nuevo_estado = request.form['estado']
    
    trabajos = leer_csv(TRABAJOS_CSV)
    vehiculos = leer_csv(VEHICULOS_CSV)
    
    for trabajo in trabajos:
        if trabajo['id'] == trabajo_id and trabajo['empresa_id'] == empresa_id:
            trabajo['estado'] = nuevo_estado
            trabajo['ultima_actualizacion'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Actualizar vehículo también
            for vehiculo in vehiculos:
                if vehiculo['id'] == trabajo['vehiculo_id']:
                    vehiculo['estado'] = nuevo_estado
                    break
            
            escribir_csv(VEHICULOS_CSV, vehiculos, 
                       ['id', 'empresa_id', 'cliente_nombre', 'cliente_email', 
                        'cliente_telefono', 'marca', 'modelo', 'año', 'color', 
                        'placa', 'vin', 'fecha_ingreso', 'estado', 'numero_orden'])
            
            break
    
    escribir_csv(TRABAJOS_CSV, trabajos, 
               ['id', 'vehiculo_id', 'empresa_id', 'numero_orden', 
                'estado', 'descripcion', 'observaciones', 'costo_estimado', 
                'fecha_inicio', 'ultima_actualizacion'])
    
    flash(f'✅ Estado actualizado a {nuevo_estado}')
    return redirect(request.referrer or url_for('dashboard_admin_empresa'))

# =============================================
# EJECUCIÓN PRINCIPAL
# =============================================

if __name__ == '__main__':
    # Inicializar sistema
    inicializar_sistema()
    
    print("=" * 60)
    print("SISTEMA DE GESTIÓN DE TALLERES - TALLER MANAGER")
    print("=" * 60)
    print("Super Administrador:")
    print("   Usuario: xonicar123")
    print("   Contraseña: xonicar123")
    print("")
    print("Estructura creada:")
    print("   • /data/ - Archivos CSV de base de datos")
    print("   • /static/fotos/ - Fotos subidas")
    print("   • /templates/ - Plantillas HTML")
    print("")
    print("Accede a: http://127.0.0.1:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)
