#!/bin/bash
# Dashboard de monitoreo completo para DocTrac
# Interfaz única para controlar toda la automatización

PROJECT_PATH="/Users/ricardovazquez/Documents/GitHub/DocTrac"
LOG_FILE="/tmp/doctrac_sync.log"
WORK_FOLDER="$HOME/Documents/Main/WorkFolder"

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
NC='\033[0m' # No Color

show_header() {
    clear
    echo -e "${BLUE}"
    echo "╔══════════════════════════════════════════════╗"
    echo "║              📋 DOCTRAC MONITOR              ║"
    echo "║         Sistema de Gestión Documental       ║"
    echo "╚══════════════════════════════════════════════╝"
    echo -e "${NC}"
}

show_status() {
    echo -e "${YELLOW}📊 ESTADO DEL SISTEMA${NC}"
    echo "═══════════════════════════════════════════════════"
    
    # Estado del cron
    if crontab -l >/dev/null 2>&1; then
        echo -e "🤖 Automatización: ${GREEN}✅ ACTIVA${NC} (cada 5 minutos)"
    else
        echo -e "🤖 Automatización: ${RED}❌ INACTIVA${NC}"
    fi
    
    # Estado de la carpeta
    PDF_COUNT=$(find "$WORK_FOLDER" -maxdepth 1 -name "*.pdf" 2>/dev/null | wc -l)
    echo -e "📁 Documentos pendientes: ${BLUE}$PDF_COUNT archivos${NC}"
    
    # Estadísticas de la base de datos
    cd "$PROJECT_PATH"
    STATS=$(.venv/bin/python manage.py shell -c "
from documents.models import Document, Category
total = Document.objects.count()
pending = Document.objects.filter(status='pending').count()
imported = Document.objects.filter(imported_from_folder=True).count()
categories = Category.objects.count()
print(f'{total}|{pending}|{imported}|{categories}')
" 2>/dev/null)
    
    if [ -n "$STATS" ]; then
        IFS='|' read -r total pending imported categories <<< "$STATS"
        echo -e "📋 Base de datos: ${GREEN}$total documentos totales${NC}"
        echo -e "⏳ Pendientes: ${YELLOW}$pending documentos${NC}"
        echo -e "📥 Importados: ${PURPLE}$imported documentos${NC}"
        echo -e "🏷️  Categorías: ${BLUE}$categories categorías${NC}"
    fi
    
    # Estado del log
    if [ -f "$LOG_FILE" ]; then
        LOG_SIZE=$(ls -lh "$LOG_FILE" | awk '{print $5}')
        LAST_ENTRY=$(tail -n 1 "$LOG_FILE")
        echo -e "📋 Log: ${GREEN}Activo${NC} ($LOG_SIZE)"
        echo -e "🕐 Última actividad: ${LAST_ENTRY}"
    else
        echo -e "📋 Log: ${YELLOW}Sin actividad${NC}"
    fi
    echo
}

show_menu() {
    echo -e "${BLUE}🔧 OPCIONES DISPONIBLES${NC}"
    echo "═══════════════════════════════════════════════════"
    echo "1) 📊 Actualizar estado"
    echo "2) 🧪 Ejecutar sincronización manual"
    echo "3) 📋 Ver logs completos"
    echo "4) 📄 Procesar todos los documentos pendientes"
    echo "5) 🚀 Activar automatización"
    echo "6) 🛑 Desactivar automatización"
    echo "7) 👀 Monitor en tiempo real"
    echo "8) 🧹 Limpiar logs"
    echo "0) ❌ Salir"
    echo
}

process_all_pending() {
    echo -e "${YELLOW}📄 PROCESANDO TODOS LOS DOCUMENTOS PENDIENTES...${NC}"
    echo "═══════════════════════════════════════════════════"
    
    # Mover todos los archivos de test_batch a WorkFolder
    if [ -d "$WORK_FOLDER/test_batch" ]; then
        BATCH_COUNT=$(find "$WORK_FOLDER/test_batch" -name "*.pdf" | wc -l)
        if [ "$BATCH_COUNT" -gt 0 ]; then
            echo -e "📥 Moviendo $BATCH_COUNT documentos de test_batch..."
            mv "$WORK_FOLDER"/test_batch/*.pdf "$WORK_FOLDER/" 2>/dev/null
        fi
    fi
    
    # Ejecutar sincronización
    cd "$PROJECT_PATH"
    ./sync_documents_enhanced.sh
    echo -e "${GREEN}✅ ¡Procesamiento completado!${NC}"
}

monitor_realtime() {
    echo -e "${GREEN}👀 MONITOR EN TIEMPO REAL${NC}"
    echo -e "${YELLOW}Presiona Ctrl+C para volver al menú${NC}"
    echo "═══════════════════════════════════════════════════"
    
    while true; do
        PDF_COUNT=$(find "$WORK_FOLDER" -maxdepth 1 -name "*.pdf" 2>/dev/null | wc -l)
        echo "$(date '+%H:%M:%S') - 📁 PDFs pendientes: $PDF_COUNT"
        
        if [ -f "$LOG_FILE" ]; then
            LAST_LOG=$(tail -n 1 "$LOG_FILE" 2>/dev/null)
            if [ -n "$LAST_LOG" ]; then
                echo "$(date '+%H:%M:%S') - 📋 $LAST_LOG"
            fi
        fi
        
        sleep 30
    done
}

# Main loop
while true; do
    show_header
    show_status
    show_menu
    
    read -p "Selecciona una opción (0-8): " choice
    
    case $choice in
        1)
            # Actualizar estado - ya se hace automáticamente
            ;;
        2)
            echo -e "${YELLOW}🧪 Ejecutando sincronización manual...${NC}"
            cd "$PROJECT_PATH"
            ./sync_documents_enhanced.sh
            read -p "Presiona Enter para continuar..."
            ;;
        3)
            echo -e "${BLUE}📋 LOGS COMPLETOS${NC}"
            echo "═══════════════════════════════════════════════════"
            if [ -f "$LOG_FILE" ]; then
                cat "$LOG_FILE"
            else
                echo "No hay logs disponibles"
            fi
            read -p "Presiona Enter para continuar..."
            ;;
        4)
            process_all_pending
            read -p "Presiona Enter para continuar..."
            ;;
        5)
            echo -e "${GREEN}🚀 Activando automatización...${NC}"
            crontab /tmp/doctrac_crontab_enhanced
            echo "✅ Automatización activada (cada 5 minutos)"
            read -p "Presiona Enter para continuar..."
            ;;
        6)
            echo -e "${RED}🛑 Desactivando automatización...${NC}"
            crontab -r 2>/dev/null
            echo "✅ Automatización desactivada"
            read -p "Presiona Enter para continuar..."
            ;;
        7)
            monitor_realtime
            ;;
        8)
            echo -e "${YELLOW}🧹 Limpiando logs...${NC}"
            rm -f "$LOG_FILE"
            echo "✅ Logs limpiados"
            read -p "Presiona Enter para continuar..."
            ;;
        0)
            echo -e "${GREEN}👋 ¡Hasta luego!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}❌ Opción inválida${NC}"
            read -p "Presiona Enter para continuar..."
            ;;
    esac
done