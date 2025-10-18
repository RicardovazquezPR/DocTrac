#!/bin/bash

# DocTrac - Script de inicio
echo "🚀 Iniciando DocTrac - Sistema de Gestión de Documentos"
echo "=================================================="

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source .venv/bin/activate

# Verificar si existen las migraciones
echo "🗄️  Verificando base de datos..."
if [ ! -f "db.sqlite3" ]; then
    echo "⚠️  Base de datos no encontrada. Creando..."
    python manage.py migrate
    echo "📊 Creando datos iniciales..."
    python manage.py setup_initial_data
else
    echo "✅ Base de datos encontrada"
fi

# Crear directorio media si no existe
if [ ! -d "media" ]; then
    echo "📁 Creando directorio para archivos..."
    mkdir media
fi

# Verificar que los archivos estáticos están configurados
echo "🎨 Configurando archivos estáticos..."
python manage.py collectstatic --noinput --clear > /dev/null 2>&1

echo ""
echo "🎉 DocTrac está listo!"
echo ""
echo "👥 Usuarios disponibles:"
echo "   Admin:    admin / admin123"
echo "   Manager:  manager1 / manager123"  
echo "   Usuario:  user1 / user123"
echo "   Usuario:  user2 / user123"
echo ""
echo "🌐 URLs importantes:"
echo "   Sistema:  http://localhost:8000/"
echo "   Admin:    http://localhost:8000/admin/"
echo ""
echo "🚀 Iniciando servidor de desarrollo..."
echo "   Presiona Ctrl+C para detener"
echo ""

# Iniciar servidor de desarrollo
python manage.py runserver