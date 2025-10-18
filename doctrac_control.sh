#!/bin/bash
# Script de control para la automatización de DocTrac
# Permite iniciar, detener y monitorear la sincronización automática

SCRIPT_DIR="/Users/ricardovazquez/Documents/GitHub/DocTrac"
LOG_FILE="/tmp/doctrac_sync.log"
PID_FILE="/tmp/doctrac_sync.pid"

case "$1" in
    start)
        echo "🚀 Iniciando automatización de DocTrac..."
        # El cron ya está configurado, solo mostramos info
        echo "✅ Cron configurado para ejecutar cada 5 minutos"
        echo "📁 Carpeta monitoreada: ~/Documents/Main/WorkFolder"
        echo "📋 Log en: $LOG_FILE"
        ;;
    
    stop)
        echo "🛑 Deshabilitando automatización de DocTrac..."
        crontab -r
        echo "✅ Cron deshabilitado"
        ;;
    
    status)
        echo "📊 ESTADO DE AUTOMATIZACIÓN"
        echo "=" * 40
        if crontab -l > /dev/null 2>&1; then
            echo "✅ Estado: Activo"
            echo "⏰ Programación: Cada 5 minutos"
            echo "📋 Log: $LOG_FILE"
            if [ -f "$LOG_FILE" ]; then
                echo "📏 Tamaño del log: $(ls -lh $LOG_FILE | awk '{print $5}')"
                echo "📅 Última entrada:"
                tail -n 1 "$LOG_FILE"
            else
                echo "📄 Log aún no creado"
            fi
        else
            echo "❌ Estado: Inactivo"
        fi
        ;;
    
    logs)
        echo "📋 LOGS DE SINCRONIZACIÓN (últimas 20 líneas)"
        echo "=" * 50
        if [ -f "$LOG_FILE" ]; then
            tail -n 20 "$LOG_FILE"
        else
            echo "📄 No hay logs disponibles aún"
        fi
        ;;
    
    test)
        echo "🧪 PRUEBA MANUAL DE SINCRONIZACIÓN"
        echo "=" * 40
        "$SCRIPT_DIR/sync_documents.sh"
        ;;
    
    monitor)
        echo "👀 MONITOREO EN TIEMPO REAL (Ctrl+C para salir)"
        echo "=" * 50
        tail -f "$LOG_FILE" 2>/dev/null &
        TAIL_PID=$!
        
        # Mostrar estado cada 30 segundos
        while true; do
            sleep 30
            echo ""
            echo "📊 $(date): Monitoreando..."
            # Contar documentos pendientes
            cd "$SCRIPT_DIR"
            PENDING=$(.venv/bin/python manage.py shell -c "
from documents.models import Document
print(Document.objects.filter(status='pending').count())
" 2>/dev/null)
            echo "⏳ Documentos pendientes: $PENDING"
        done
        ;;
    
    *)
        echo "🔧 CONTROL DE AUTOMATIZACIÓN DOCTRAC"
        echo "=" * 40
        echo "Uso: $0 {start|stop|status|logs|test|monitor}"
        echo ""
        echo "Comandos disponibles:"
        echo "  start   - Activar automatización (cada 5 minutos)"
        echo "  stop    - Desactivar automatización"
        echo "  status  - Ver estado actual"
        echo "  logs    - Ver logs recientes"
        echo "  test    - Ejecutar sincronización manual"
        echo "  monitor - Monitorear en tiempo real"
        echo ""
        echo "Ejemplos:"
        echo "  $0 start     # Activar automático"
        echo "  $0 test      # Probar manualmente"
        echo "  $0 status    # Ver si está funcionando"
        ;;
esac