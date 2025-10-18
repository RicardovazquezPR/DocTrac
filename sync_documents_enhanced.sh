#!/bin/bash
# Script mejorado de sincronización con notificaciones y mejores logs
# Este script reemplaza el anterior con más funcionalidades

# Configuración
PROJECT_PATH="/Users/ricardovazquez/Documents/GitHub/DocTrac"
VENV_PATH="$PROJECT_PATH/.venv/bin/python"
LOG_FILE="/tmp/doctrac_sync.log"
WORK_FOLDER="$HOME/Documents/Main/WorkFolder"

# Función para logging con timestamp
log() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" | tee -a "$LOG_FILE"
}

# Cambiar al directorio del proyecto
cd "$PROJECT_PATH"

# Verificar que existe la carpeta de monitoreo
if [ ! -d "$WORK_FOLDER" ]; then
    log "❌ ERROR: No existe la carpeta de monitoreo: $WORK_FOLDER"
    exit 1
fi

# Contar archivos PDF antes de la sincronización
PDF_COUNT=$(find "$WORK_FOLDER" -maxdepth 1 -name "*.pdf" | wc -l)

if [ "$PDF_COUNT" -eq 0 ]; then
    log "✅ No hay documentos nuevos para procesar"
else
    log "📄 Encontrados $PDF_COUNT documentos para procesar"
    
    # Ejecutar la sincronización y capturar la salida
    SYNC_OUTPUT=$($VENV_PATH manage.py sync_documents 2>&1)
    SYNC_EXIT_CODE=$?
    
    if [ $SYNC_EXIT_CODE -eq 0 ]; then
        # Contar documentos procesados de la salida
        PROCESSED_COUNT=$(echo "$SYNC_OUTPUT" | grep "✅ Procesados" | grep -o '[0-9]* documentos nuevos' | grep -o '[0-9]*')
        
        if [ -n "$PROCESSED_COUNT" ] && [ "$PROCESSED_COUNT" -gt 0 ]; then
            log "🎉 ¡Sincronización exitosa! Procesados $PROCESSED_COUNT documentos"
            
            # Obtener estadísticas actualizadas del sistema
            STATS_OUTPUT=$($VENV_PATH manage.py shell -c "
from documents.models import Document
pending = Document.objects.filter(status='pending').count()
total = Document.objects.count()
imported = Document.objects.filter(imported_from_folder=True).count()
print(f'Total:{total},Pendientes:{pending},Importados:{imported}')
" 2>/dev/null)
            
            if [ -n "$STATS_OUTPUT" ]; then
                log "📊 Estado actual: $STATS_OUTPUT"
            fi
        else
            log "ℹ️ No se procesaron documentos nuevos"
        fi
    else
        log "❌ Error en la sincronización: $SYNC_OUTPUT"
    fi
fi

# Limpiar logs antiguos si son muy grandes (más de 50MB)
if [ -f "$LOG_FILE" ]; then
    LOG_SIZE=$(stat -f%z "$LOG_FILE" 2>/dev/null || echo "0")
    if [ "$LOG_SIZE" -gt 52428800 ]; then  # 50MB
        tail -n 1000 "$LOG_FILE" > "$LOG_FILE.tmp"
        mv "$LOG_FILE.tmp" "$LOG_FILE"
        log "🧹 Log limpiado - mantenidas las últimas 1000 líneas"
    fi
fi