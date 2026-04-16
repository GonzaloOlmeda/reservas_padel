# 🏓 RESERVAS_PADEL - Sistema de Reservas de Pistas de Pádel

Una aplicación web completa desarrollada con Django para gestionar reservas de pistas de pádel, sistema de créditos/bonos, autenticación de usuarios y notificaciones por email.

## 📋 Tabla de Contenidos

- [Descripción del Proyecto](#descripción-del-proyecto)
- [Características Principales](#características-principales)
- [Requisitos Previos](#requisitos-previos)
- [Instalación](#instalación)
- [Migraciones de Base de Datos](#migraciones-de-base-de-datos)
- [Creación de Usuarios](#creación-de-usuarios)
- [Ejecutar el Servidor](#ejecutar-el-servidor)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [URLs Principales](#urls-principales)
- [Sistema de Bonos de Créditos](#sistema-de-bonos-de-créditos)
- [Sistema de Notificaciones por Email](#sistema-de-notificaciones-por-email)
- [Descripción de las Apps](#descripción-de-las-apps)

---

## 📌 Descripción del Proyecto

**RESERVAS_PADEL** es una solución integral para administrar reservas de pistas de pádel. El sistema permite que los usuarios se registren, compren bonos de créditos, realicen reservas en diferentes pistas y reciban confirmaciones por email. Los administradores pueden gestionar pistas, horarios, usuarios y reservas desde el panel de administración de Django.

**Caso de Uso:**
- Un usuario se registra en la plataforma
- Compra un bono de créditos (por ejemplo, 10 créditos)
- Reserva una pista para una fecha y hora específica
- El sistema consume 1 crédito por cada reserva
- El usuario recibe confirmación por email
- El usuario puede cancelar reservas y recuperar los créditos

---

## ✨ Características Principales

### 🔐 Autenticación y Usuarios
- Registro de usuarios con email
- Sistema de login seguro
- Perfil de usuario con historial de reservas
- Model personalizado de usuario con roles
- Logout con confirmación

### 🎫 Sistema de Bonos y Créditos
- Compra de bonos con diferentes paquetes de créditos
- Consumo automático de 1 crédito por reserva
- Visualización de créditos disponibles
- Validación de créditos before de reservar
- Recuperación de créditos al cancelar reservas

### 📅 Sistema de Reservas
- Visualización de pistas disponibles
- Selección de fecha y horario
- Reserva con validación de disponibilidad
- Cancelación de reservas futuras
- Historial de reservas del usuario

### 📧 Notificaciones por Email
- Email de bienvenida al registro
- Confirmación de reserva
- Confirmación de cancelación
- Confirmación de compra de bono
- Backend configurable (consola en desarrollo, SMTP en producción)

### 👨‍💼 Panel de Administración
- Gestión completa de pistas
- Gestión de horarios
- Gestión de usuarios
- Gestión de bonos
- Gestión de reservas
- Vista de historial

---

## 🔧 Requisitos Previos

Antes de instalar el proyecto, asegúrate de tener lo siguiente:

- **Python 3.10 o superior** (verificar con `python --version`)
- **pip** (gestor de paquetes de Python)
- **Git** (para clonar el repositorio)
- **SQLite3** (incluido con Python)

---

## 📥 Instalación

### Paso 1: Clonar el Repositorio

```bash
git clone <url-del-repositorio>
cd reservas_padel
```

### Paso 2: Crear un Entorno Virtual

```bash
# En Windows
python -m venv venv
venv\Scripts\activate

# En macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

### Paso 3: Instalar Dependencias

```bash
pip install -r reservas/requirements.txt
```

Las dependencias principales incluyen:
- **Django 5.2.8** - Framework web
- **Django REST Framework 3.16.1** - API REST (opcional)

### Paso 4: Configurar Variables de Entorno (Opcional)

Crea un archivo `.env` en la raíz del proyecto para configuraciones sensibles:

```env
DEBUG=True
SECRET_KEY=tu-clave-secreta-aqui
ALLOWED_HOSTS=localhost,127.0.0.1
```

Luego modifica `config/settings.py` para cargar estas variables:

```python
from dotenv import load_dotenv
load_dotenv()
```

---

## 🔄 Migraciones de Base de Datos

Las migraciones crean las tablas y esquema necesario en la base de datos.

### Paso 1: Aplicar Migraciones

```bash
python manage.py migrate
```

Este comando aplicará todas las migraciones pendientes:
- `usuarios/migrations/0001_initial.py` - Tabla de usuarios personalizado
- `usuarios/migrations/0002_initial.py` - Campos adicionales de usuario
- `reservas/migrations/0001_initial.py` - Tablas de pistas, horarios y bonos
- `reservas/migrations/0002_initial.py` - Tabla de reservas

### Paso 2: Verificar Instalación

```bash
python manage.py check
```

Si el comando completa sin errores, ¡la instalación es correcta!

---

## 👥 Creación de Usuarios

### Usuario Administrativo (Superusuario)

Para acceder al panel de administración, crea un superusuario:

```bash
python manage.py createsuperuser
```

Te pedirá:
- **Username**: Nombre de usuario (ej: `admin`)
- **Email**: Tu email (ej: `admin@padel.com`)
- **Password**: Contraseña (mínimo 8 caracteres recomendado)
- **Password (again)**: Confirma la contraseña

**Credenciales de Prueba Recomendadas:**
```
Username: admin
Email: admin@padel.com
Password: Administrador123!
```

### Crear Usuario desde la Shell de Django

```bash
python manage.py shell
```

```python
from usuarios.models import Usuario

# Crear usuario
usuario = Usuario.objects.create_user(
    username='juan',
    email='juan@example.com',
    password='password123',
    first_name='Juan',
    last_name='Pérez'
)
print(f"Usuario creado: {usuario.username}")
```

---

## 🚀 Ejecutar el Servidor

### Iniciar el Servidor de Desarrollo

```bash
python manage.py runserver
```

El servidor se iniciará en: **http://127.0.0.1:8000/**

En la terminal verás:
```
Django version 5.2.8, using settings 'config.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CTRL-BREAK.
```

### Acceder a la Aplicación

- **Home**: http://127.0.0.1:8000/
- **Registro**: http://127.0.0.1:8000/registro/
- **Login**: http://127.0.0.1:8000/login/
- **Panel Admin**: http://127.0.0.1:8000/admin/

---

## 📁 Estructura del Proyecto

```
reservas_padel/
├── manage.py                          # Herramienta de gestión de Django
├── db.sqlite3                         # Base de datos (SQLite)
├── README.md                          # Este archivo
├── config/
│   ├── __init__.py
│   ├── settings.py                    # Configuración de Django
│   ├── urls.py                        # URLs principales
│   ├── asgi.py                        # Configuración ASGI
│   └── wsgi.py                        # Configuración WSGI
├── reservas/
│   ├── migrations/
│   │   ├── 0001_initial.py           # Migración inicial
│   │   └── 0002_initial.py           # Migración modelos relacionales
│   ├── templates/
│   │   ├── base.html                 # Template base
│   │   ├── reservas/
│   │   │   ├── home.html             # Home del usuario
│   │   │   ├── reservar.html         # Formulario de reserva
│   │   │   ├── mis_reservas.html     # Listado de reservas del usuario
│   │   │   ├── comprar_bono.html     # Compra de bonos
│   │   │   └── cancelar.html         # Cancelación de reservas
│   │   └── usuarios/
│   │       └── perfil.html           # Perfil del usuario
│   ├── static/                        # Archivos estáticos (CSS, JS, imágenes)
│   ├── __init__.py
│   ├── admin.py                       # Configuración del admin
│   ├── apps.py                        # Configuración de la app
│   ├── models.py                      # Modelos (Pista, Reserva, Bono, Horario)
│   ├── urls.py                        # URLs de la app reservas
│   ├── views.py                       # Vistas y lógica de reservas
│   ├── forms.py                       # Formularios
│   ├── tests.py                       # Tests unitarios
│   └── requirements.txt               # Dependencias del proyecto
└── usuarios/
    ├── migrations/
    │   ├── 0001_initial.py
    │   └── 0002_initial.py
    ├── templates/
    │   └── usuarios/
    │       ├── registro.html          # Formulario de registro
    │       ├── login.html             # Formulario de login
    │       └── perfil.html            # Perfil del usuario
    ├── __init__.py
    ├── admin.py                       # Usuario en el admin
    ├── apps.py                        # Configuración de la app
    ├── models.py                      # Modelo Usuario personalizado
    ├── urls.py                        # URLs de la app usuarios
    ├── views.py                       # Vistas de autenticación
    ├── forms.py                       # Formularios de registro y login
    ├── tests.py                       # Tests unitarios
    └── migrations/
        └── ...
```

---

## 🌐 URLs Principales

### Rutas de Usuarios (usuarios/)

| URL | Método | Descripción |
|-----|--------|-------------|
| `/registro/` | GET, POST | Formulario y procesamiento de registro |
| `/login/` | GET, POST | Formulario y procesamiento de login |
| `/logout/` | POST | Cerrar sesión |
| `/perfil/` | GET | Perfil del usuario conectado |

### Rutas de Reservas (reservas/)

| URL | Método | Descripción |
|-----|--------|-------------|
| `/` | GET | Página de inicio con listado de pistas |
| `/<pista_id>/reservar/` | GET, POST | Reservar una pista |
| `/mis-reservas/` | GET | Listado de las reservas del usuario |
| `/<reserva_id>/cancelar/` | GET, POST | Cancelar una reserva |
| `/comprar-bono/` | GET, POST | Comprar un bono de créditos |
| `/crear-reserva/` | POST | API para crear reserva (JSON) |

### Rutas del Admin

| URL | Descripción |
|-----|-------------|
| `/admin/` | Panel de administración |
| `/admin/usuarios/usuario/` | Gestión de usuarios |
| `/admin/reservas/pista/` | Gestión de pistas |
| `/admin/reservas/horario/` | Gestión de horarios |
| `/admin/reservas/bono/` | Gestión de bonos |
| `/admin/reservas/reserva/` | Gestión de reservas |

---

## 💰 Sistema de Bonos de Créditos

### ¿Cómo Funciona?

1. **Compra de Bono**: El usuario compra un bono que contiene cierta cantidad de créditos
   - Paquete Básico: 5 créditos
   - Paquete Estándar: 10 créditos
   - Paquete Premium: 20 créditos

2. **Consumo**: Cada reserva consume 1 crédito
   - Validación: No se permite reservar sin créditos disponibles
   - Deducción: Se deduce automáticamente al crear la reserva

3. **Recuperación**: Al cancelar una reserva, se devuelven los créditos
   - El usuario recupera 1 crédito
   - El bono se reactiva si fue su último crédito

4. **Visualización**: El usuario ve sus créditos disponibles en:
   - Perfil del usuario
   - Página de inicio
   - Email de confirmación de reservas

### Modelos Relacionados

**Bono**
```python
class Bono(models.Model):
    usuario = ForeignKey(Usuario)
    creditos = IntegerField()
    activo = BooleanField()
    fecha_compra = DateTimeField(auto_now_add=True)
```

**Reserva**
```python
class Reserva(models.Model):
    usuario = ForeignKey(Usuario)
    pista = ForeignKey(Pista)
    fecha = DateField()
    horario = ForeignKey(Horario)
    estado = CharField(choices=['activa', 'cancelada'])
```

---

## 📧 Sistema de Notificaciones por Email

### Configuración

**Backend de Email** (en `config/settings.py`):

```python
# Desarrollo (muestra emails en consola)
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# Producción (usa SMTP)
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'tu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'tu-contraseña-app'
```

### Emails Enviados

#### 1. Email de Bienvenida (Registro)
**Cuándo**: Al completar el registro
**Destinatario**: Nuevo usuario
**Contenido**:
- Mensaje de bienvenida
- Instrucciones para comprar un bono
- Link a la plataforma

#### 2. Email de Confirmación de Reserva
**Cuándo**: Al reservar una pista
**Destinatario**: Usuario que reservó
**Contenido**:
- Nombre de pista
- Fecha y hora
- Créditos restantes
- Opción de cancelación

#### 3. Email de Cancelación de Reserva
**Cuándo**: Al cancelar una reserva
**Destinatario**: Usuario que canceló
**Contenido**:
- Detalles de la reserva cancelada
- Créditos devueltos/restantes
- Opción de hacer nueva reserva

#### 4. Email de Compra de Bono
**Cuándo**: Al comprar un bono de créditos
**Destinatario**: Usuario que compró
**Contenido**:
- Créditos comprados
- Créditos totales disponibles
- Acceso a reservas

### Manejo de Errores

Todos los envíos de email tienen `fail_silently=True`, lo que significa:
- Si falla el envío de email, NO se rompe la funcionalidad
- Se registra el error en consola
- La reserva/compra se completa normalmente

---

## 📚 Descripción de las Apps

### App: `usuarios`

**Propósito**: Gestión de autenticación y perfiles de usuario

**Modelos**:
```python
class Usuario(AbstractUser):
    email = EmailField(unique=True)
    rol = CharField(choices=[
        ('cliente', 'Cliente'),
        ('admin', 'Administrador')
    ])
    fecha_registro = DateTimeField(auto_now_add=True)
```

**Vistas**:
- `registro()` - Registro de nuevos usuarios
- `login_view()` - Login de usuarios
- `logout_view()` - Logout
- `perfil()` - Perfil del usuario con historial

**Formularios**:
- `RegistroForm` - Validación de registro
- `LoginForm` - Validación de login

**URLs**:
- `/registro/` - GET/POST
- `/login/` - GET/POST
- `/logout/` - POST
- `/perfil/` - GET

### App: `reservas`

**Propósito**: Gestión de pistas, reservas y bonos

**Modelos**:
```python
class Pista(models.Model):
    nombre = CharField(max_length=100)
    descripcion = TextField()
    activa = BooleanField()
    
class Horario(models.Model):
    pista = ForeignKey(Pista)
    hora_inicio = TimeField()
    hora_fin = TimeField()
    
class Bono(models.Model):
    usuario = ForeignKey(Usuario)
    creditos = IntegerField()
    activo = BooleanField()
    
class Reserva(models.Model):
    usuario = ForeignKey(Usuario)
    pista = ForeignKey(Pista)
    horario = ForeignKey(Horario)
    fecha = DateField()
    estado = CharField()
```

**Vistas**:
- `home()` - Listado de pistas disponibles
- `crear_reserva()` - Crear reserva (API JSON)
- `reservar_pista()` - Reservar pista específica
- `mis_reservas()` - Historial de reservas del usuario
- `cancelar_reserva()` - Cancelar reserva
- `comprar_bono()` - Comprar bonos de créditos

**URLs**:
- `/` - Home
- `/<pista_id>/reservar/` - Reservar pista
- `/mis-reservas/` - Mis reservas
- `/<reserva_id>/cancelar/` - Cancelar
- `/comprar-bono/` - Comprar bono

---

## 🧪 Pruebas

### Ejecutar Tests

```bash
# Todos los tests
python manage.py test

# Tests de usuarios
python manage.py test usuarios

# Tests de reservas
python manage.py test reservas

# Tests con verbosidad
python manage.py test --verbosity=2
```

### Crear Datos de Prueba

```bash
python manage.py shell
```

```python
from reservas.models import Pista, Horario
from datetime import time

# Crear pista
pista = Pista.objects.create(
    nombre="Pista 1",
    descripcion="Pista exterior techada",
    activa=True
)

# Crear horarios
Horario.objects.create(pista=pista, hora_inicio=time(9,0), hora_fin=time(10,0))
Horario.objects.create(pista=pista, hora_inicio=time(10,0), hora_fin=time(11,0))
```

---

## 🛠️ Solución de Problemas

### Error: "ModuleNotFoundError: No module named 'django'"

**Solución**: Asegúrate de haber activado el entorno virtual y instalado dependencias:
```bash
pip install -r reservas/requirements.txt
```

### Error: "No such table: usuarios_usuario"

**Solución**: Aplicar migraciones:
```bash
python manage.py migrate
```

### Error: "PermissionError: Database is locked"

**Solución**: Cierra otras instancias de Django y borra el archivo `db.sqlite3`:
```bash
rm db.sqlite3
python manage.py migrate
```

### Los emails no se envían

**Verificación**:
1. Verifica que `EMAIL_BACKEND` esté configurado
2. En desarrollo, los emails aparecen en la consola
3. En producción, verifica las credenciales SMTP

---

## 📝 Notas de Desarrollo

### Cambios Recientes

- **v1.0.0**: Sistema completo de reservas, bonos y autenticación
- **Email Notifications**: Sistema de notificaciones por email implementado
- **Admin Panel**: Panel de administración totalmente funcional

**Última actualización**: Abril 2026  
**Versión de Django**: 5.2.8  
**Versión de Python**: 3.10+
