#!/bin/bash
# Script de inicio mejorado con configuración de tipo de uso

PROJECT_PATH="/Users/ricardovazquez/Documents/GitHub/DocTrac"
VENV_PATH="$PROJECT_PATH/.venv/bin/python"

# Colores
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${BLUE}🚀 DOCTRAC - SISTEMA DE GESTIÓN DOCUMENTAL${NC}"
echo "================================================="

cd "$PROJECT_PATH"

# Verificar configuración actual
USAGE_TYPE=$($VENV_PATH manage.py shell -c "
from django.conf import settings
print(getattr(settings, 'SYSTEM_USAGE_TYPE', 'personal'))
" 2>/dev/null)

echo -e "${YELLOW}📋 Configuración actual: $USAGE_TYPE${NC}"

# Preguntar si quiere cambiar la configuración
if [ "$1" != "--skip-config" ]; then
    echo ""
    echo "¿Qué tipo de uso deseas configurar?"
    echo "1) 👤 Personal (personas y empresas)"
    echo "2) 🏢 Empresa (departamentos internos)"
    echo "3) ⏩ Continuar con configuración actual ($USAGE_TYPE)"
    echo ""
    read -p "Selecciona una opción (1-3): " config_choice

    case $config_choice in
        1)
            echo -e "${YELLOW}Configurando modo personal...${NC}"
            $VENV_PATH manage.py setup_usage_type personal
            $VENV_PATH manage.py create_sample_entities
            ;;
        2)
            echo -e "${YELLOW}Configurando modo empresa...${NC}"
            $VENV_PATH manage.py setup_usage_type empresa
            $VENV_PATH manage.py create_sample_entities
            ;;
        3|*)
            echo -e "${GREEN}Continuando con configuración actual...${NC}"
            ;;
    esac
fi

echo ""
echo -e "${GREEN}🔧 Iniciando servicios...${NC}"

# Ejecutar migraciones
echo "📝 Aplicando migraciones..."
$VENV_PATH manage.py migrate --noinput

# Crear superusuario si no existe
echo "👤 Verificando usuario administrador..."
$VENV_PATH manage.py shell -c "
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(is_superuser=True).exists():
    print('Creando usuario administrador...')
    User.objects.create_superuser('admin', 'admin@doctrac.com', 'admin123')
    print('✅ Usuario admin creado (admin/admin123)')
else:
    print('✅ Usuario administrador ya existe')
" 2>/dev/null

# Ejecutar datos iniciales
echo "📊 Configurando datos iniciales..."
$VENV_PATH manage.py setup_initial_data

echo ""
echo -e "${BLUE}📊 ESTADO DEL SISTEMA:${NC}"
$VENV_PATH manage.py shell -c "
from documents.models import Document, Category, Person
from django.conf import settings

print(f'📋 Documentos: {Document.objects.count()}')
print(f'🏷️  Categorías: {Category.objects.count()}')
print(f'👥 Personas/Departamentos: {Person.objects.count()}')

usage_type = getattr(settings, 'SYSTEM_USAGE_TYPE', 'personal')
print(f'⚙️  Tipo de uso: {usage_type}')

if usage_type == 'empresa':
    dept_count = Person.objects.filter(is_department=True).count()
    company_count = Person.objects.filter(is_company=True, is_department=False).count()
    print(f'🏢 Departamentos: {dept_count}')
    print(f'🏭 Empresas externas: {company_count}')
else:
    person_count = Person.objects.filter(is_company=False).count()
    company_count = Person.objects.filter(is_company=True).count()
    print(f'👤 Personas: {person_count}')
    print(f'🏢 Empresas: {company_count}')
" 2>/dev/null

echo ""
echo -e "${GREEN}🌐 Iniciando servidor web...${NC}"
echo -e "${YELLOW}Accede a: http://127.0.0.1:8000/${NC}"
echo -e "${YELLOW}Usuario: admin / Contraseña: admin123${NC}"
echo ""
echo "Presiona Ctrl+C para detener el servidor"

# Iniciar servidor
$VENV_PATH manage.py runserver