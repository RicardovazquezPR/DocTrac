# 📄 DocTrac - Sistema de Gestión de Documentos PDF

**DocTrac** es un sistema web moderno desarrollado en Django para la gestión, organización y visualización de documentos PDF con una interfaz intuitiva de 3 columnas.

## 🚀 Características Principales

### 📋 Gestión de Documentos
- ✅ **Subida de archivos PDF** con validación automática
- ✅ **Visualización integrada** de PDFs en navegador
- ✅ **Categorización dinámica** por tipos y categorías
- ✅ **Estados de documento** (pendiente, aprobado, revisión)
- ✅ **Sistema de etiquetado** personalizable
- ✅ **Historial de cambios** completo

### 🎨 Interfaz de Usuario
- ✅ **Diseño responsivo** con Bootstrap 5
- ✅ **Interfaz de 3 columnas**:
  - 25% - Lista de documentos pendientes
  - 50% - Visualizador de PDF
  - 25% - Panel de categorización
- ✅ **Iconografía Font Awesome**
- ✅ **Experiencia AJAX** sin recargas

### 👥 Sistema de Usuarios
- ✅ **Autenticación segura** con Django Auth
- ✅ **Roles diferenciados** (Admin, Manager, Employee, Viewer)
- ✅ **Control de permisos** granular
- ✅ **Asignación de documentos** a usuarios

### 📊 Funcionalidades Avanzadas
- ✅ **Nombres estructurados automáticos**
- ✅ **Panel administrativo** completo
- ✅ **Búsqueda y filtrado** inteligente
- ✅ **API endpoints** RESTful
- ✅ **Logging detallado**

## 🛠️ Tecnologías Utilizadas

- **Backend**: Django 5.0.8, Python 3.13+
- **Frontend**: Bootstrap 5, jQuery, Font Awesome
- **Base de datos**: SQLite (desarrollo), compatible con PostgreSQL/MySQL
- **Almacenamiento**: Sistema de archivos local
- **Autenticación**: Django Auth System

## 📦 Instalación

### Prerrequisitos
- Python 3.13+
- Git

### Pasos de instalación

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/ricardovazquez/DocTrac.git
   cd DocTrac
   ```

2. **Crear entorno virtual**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # En Windows: .venv\Scripts\activate
   ```

3. **Instalar dependencias**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar base de datos**
   ```bash
   python manage.py migrate
   ```

5. **Crear datos iniciales**
   ```bash
   python manage.py setup_initial_data
   ```

6. **Iniciar servidor**
   ```bash
   python manage.py runserver
   ```

7. **Acceder al sistema**
   - URL: `http://127.0.0.1:8000`
   - Usuario admin: `admin`
   - Contraseña: `admin123`

## 🎯 Uso del Sistema

### Dashboard Principal
1. **Visualizar documentos**: Lista de documentos pendientes en columna izquierda
2. **Seleccionar documento**: Click en cualquier documento para cargarlo
3. **Ver PDF**: Visualización automática en panel central
4. **Categorizar**: Usar panel derecho para asignar categorías, tipos, etc.
5. **Guardar cambios**: Botón "Guardar Cambios" para persistir modificaciones

### Gestión de Documentos
- **Nuevo Documento**: Botón "Nuevo Documento" en navbar
- **Lista Completa**: Enlace "Documentos" para vista de tabla
- **Administración**: Enlace "Admin" para panel administrativo

### Controles de PDF
- **Nueva Pestaña**: Abrir PDF en pestaña separada
- **Recargar**: Refrescar visualizador si hay problemas
- **Descargar**: Download directo del archivo

## 📁 Estructura del Proyecto

```
DocTrac/
├── 📁 accounts/          # App de autenticación
├── 📁 documents/         # App principal de documentos
│   ├── 📄 models.py      # Modelos de BD
│   ├── 📄 views.py       # Vistas y lógica
│   ├── 📄 urls.py        # URLs de la app
│   └── 📁 management/    # Comandos personalizados
├── 📁 media/             # Archivos subidos
├── 📁 static/            # Archivos estáticos
│   ├── 📁 css/           # Estilos personalizados
│   └── 📁 js/            # JavaScript personalizado
├── 📁 templates/         # Templates HTML
├── 📄 manage.py          # Script de Django
├── 📄 requirements.txt   # Dependencias
└── 📄 README.md          # Esta documentación
```

## 🔧 Configuración

### Variables de Entorno (Opcional)
```bash
# .env file
DEBUG=True
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///db.sqlite3
```

### Configuración de Production
Para producción, modificar `settings.py`:
- `DEBUG = False`
- Configurar base de datos apropiada
- Configurar archivos estáticos
- Configurar dominio permitido

## 🤝 Contribución

1. Fork el proyecto
2. Crear branch de feature (`git checkout -b feature/AmazingFeature`)
3. Commit cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push al branch (`git push origin feature/AmazingFeature`)
5. Abrir Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 👨‍💻 Autor

**Ricardo Vázquez**
- GitHub: [@ricardovazquez](https://github.com/ricardovazquez)

## 🙏 Agradecimientos

- Django Community
- Bootstrap Team
- Font Awesome
- VS Code Team por las excelentes herramientas de desarrollo

---

⭐ **¡Si te gusta este proyecto, dale una estrella!** ⭐

DocTrac es un sistema Django completo para organizar y gestionar documentos PDF con una interfaz de 3 columnas, sistema de usuarios con permisos, categorización inteligente e historial de cambios.

## Características Principales

### 🗂️ Interfaz de 3 Columnas
- **Izquierda (25%)**: Lista de documentos pendientes de organizar
- **Centro (50%)**: Vista previa del documento PDF activo
- **Derecha (25%)**: Panel de categorización con dropdowns dependientes

### 👥 Sistema de Usuarios y Permisos
- **Administrador**: Acceso completo a todos los documentos
- **Gerente**: Puede ver documentos asignados y gestionar usuarios
- **Usuario**: Solo ve documentos que se le asignen específicamente

### 📊 Categorización Inteligente
- Categorías y tipos de documento jerárquicos
- Asociación con personas o empresas
- Estados de documento (pendiente, escaneado, digitalizado, etc.)
- Estados de pago (pagado, pendiente, vencido)
- Generación automática de nombres estructurados

### 📝 Historial de Estados
- Seguimiento completo de cambios de estado
- Registro de quién y cuándo realizó cada cambio
- Motivos de los cambios de estado

## Instalación y Configuración

### Prerrequisitos
- Python 3.8+
- pip (gestor de paquetes de Python)

### Pasos de Instalación

1. **Clonar/Descargar el proyecto**
   ```bash
   # Si tienes el código, navega al directorio
   cd DocTrac
   ```

2. **Activar el entorno virtual** (ya configurado)
   ```bash
   source .venv/bin/activate  # En macOS/Linux
   # o
   .venv\\Scripts\\activate  # En Windows
   ```

3. **Instalar dependencias** (ya instaladas)
   ```bash
   pip install Django==5.0.8 Pillow==10.4.0 python-magic==0.4.27
   ```

4. **Configurar la base de datos** (ya ejecutado)
   ```bash
   python manage.py migrate
   python manage.py setup_initial_data
   ```

5. **Iniciar el servidor de desarrollo**
   ```bash
   python manage.py runserver
   ```

6. **Acceder al sistema**
   - Sistema principal: http://localhost:8000/
   - Panel de administración: http://localhost:8000/admin/

## Usuarios de Prueba

El comando `setup_initial_data` crea los siguientes usuarios:

| Usuario    | Contraseña  | Rol           | Descripción                    |
|------------|-------------|---------------|--------------------------------|
| admin      | admin123    | Administrador | Acceso completo al sistema     |
| manager1   | manager123  | Gerente       | Gestión de documentos          |
| user1      | user123     | Usuario       | Solo documentos asignados      |
| user2      | user123     | Usuario       | Solo documentos asignados      |

## Estructura del Proyecto

```
DocTrac/
├── doctrac/                 # Configuración principal del proyecto
│   ├── settings.py         # Configuración de Django
│   ├── urls.py            # URLs principales
│   └── wsgi.py            # Configuración WSGI
├── accounts/               # Aplicación de usuarios
│   ├── models.py          # Modelo de usuario personalizado
│   ├── views.py           # Vistas de autenticación
│   └── admin.py           # Configuración del admin
├── documents/              # Aplicación principal de documentos
│   ├── models.py          # Modelos de documentos, categorías, etc.
│   ├── views.py           # Vistas del sistema
│   ├── admin.py           # Configuración del admin
│   ├── signals.py         # Señales para historial automático
│   ├── permissions.py     # Sistema de permisos
│   └── management/        # Comandos personalizados
├── templates/              # Plantillas HTML
│   ├── base.html          # Plantilla base
│   ├── accounts/          # Plantillas de autenticación
│   └── documents/         # Plantillas de documentos
├── static/                 # Archivos estáticos
│   ├── css/main.css       # Estilos personalizados
│   └── js/main.js         # JavaScript funcional
└── media/                  # Archivos subidos (PDFs)
```

## Uso del Sistema

### 1. Iniciar Sesión
- Accede a http://localhost:8000/
- Usa cualquiera de los usuarios de prueba
- Serás redirigido al dashboard principal

### 2. Dashboard Principal
- **Lista de Documentos**: Haz clic en cualquier documento pendiente
- **Vista Previa**: El PDF se mostrará en el centro
- **Categorización**: Usa el panel derecho para categorizar

### 3. Subir Nuevos Documentos
- Click en "Nuevo Documento" en la barra de navegación
- Sube un archivo PDF y completa la información
- El documento aparecerá en la lista de pendientes

### 4. Categorizar Documentos
1. Selecciona una **categoría**
2. Elige un **tipo de documento** (se cargan dinámicamente)
3. Asocia con una **persona o empresa**
4. Establece la **fecha del documento**
5. Define el **estado de pago** si aplica
6. Cambia el **estado** del documento
7. Agrega **notas** si es necesario
8. Guarda los cambios

### 5. Sistema de Permisos
- **Administradores**: Ven todos los documentos
- **Usuarios regulares**: Solo ven documentos asignados a ellos
- **Asignación**: Se hace desde el panel de admin o al crear documentos

### 6. Historial de Cambios
- Cada cambio de estado se registra automáticamente
- Incluye usuario, fecha, estado anterior y nuevo
- Visible en la vista detalle de cada documento

## Datos Iniciales Incluidos

### Categorías
- Facturas
- Contratos  
- Recursos Humanos
- Finanzas
- Legal
- Administrativo

### Tipos de Documento (ejemplos)
- Factura de Venta/Compra
- Contratos de Servicios
- Estados de Cuenta
- Oficios y Memorándums
- Y muchos más...

### Personas y Empresas de Ejemplo
- Varias personas físicas
- Empresas con datos completos
- Listas para usar en las categorizaciones

## Personalización

### Agregar Nuevas Categorías
1. Ve al admin: http://localhost:8000/admin/
2. Sección "Documents" → "Categorías"
3. Agrega nuevas categorías

### Crear Tipos de Documento
1. Admin → "Documents" → "Tipos de Documentos" 
2. Asocia cada tipo con una categoría

### Gestionar Usuarios
1. Admin → "Accounts" → "Users"
2. Crea usuarios y asigna roles
3. Los permisos se aplican automáticamente

## Comandos Útiles

```bash
# Crear nuevas migraciones después de cambios en modelos
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario adicional
python manage.py createsuperuser

# Recargar datos iniciales (cuidado: puede duplicar)
python manage.py setup_initial_data

# Ejecutar servidor de desarrollo
python manage.py runserver

# Ejecutar en puerto específico
python manage.py runserver 8080
```

## Tecnologías Utilizadas

- **Backend**: Django 5.0.8
- **Frontend**: Bootstrap 5.3, Font Awesome, jQuery
- **Base de Datos**: SQLite (desarrollo) - fácil cambio a PostgreSQL/MySQL
- **Archivos**: Pillow para manejo de imágenes, python-magic para validación

## Características Técnicas

### Seguridad
- Autenticación requerida para todas las vistas
- Sistema de permisos granular por documento
- Validación CSRF en formularios AJAX
- Validación de tipos de archivo (solo PDFs)

### Rendimiento
- Consultas optimizadas con select_related()
- Lazy loading para imágenes
- Paginación en listas de documentos
- Archivos estáticos optimizados

### Experiencia de Usuario
- Interfaz responsive (funciona en móviles)
- Dropdowns dependientes con AJAX
- Vista previa de PDF integrada
- Notificaciones en tiempo real
- Shortcuts de teclado (Ctrl+S para guardar)

## Próximas Mejoras Sugeridas

- [ ] Búsqueda avanzada con filtros
- [ ] Exportación de reportes
- [ ] Notificaciones por email
- [ ] Integración con escáner
- [ ] API REST completa
- [ ] Dashboard con estadísticas
- [ ] Backup automático de documentos
- [ ] OCR para extraer texto de PDFs

## Soporte

Para dudas o problemas:
1. Revisa los logs de Django en la consola
2. Verifica permisos de archivos en `/media`
3. Consulta la documentación de Django para configuraciones avanzadas

## Licencia

Este proyecto es de código abierto y puede ser modificado según las necesidades específicas de tu organización.

---

**¡DocTrac está listo para usar!** 🚀

Inicia el servidor con `python manage.py runserver` y comienza a organizar tus documentos PDF de manera profesional.