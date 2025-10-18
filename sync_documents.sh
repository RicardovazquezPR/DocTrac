#!/bin/bash
# Script de sincronización automática de documentos
# Este script se ejecuta periódicamente para importar documentos nuevos

# Ruta del proyecto Django
PROJECT_PATH="/Users/ricardovazquez/Documents/GitHub/DocTrac"
VENV_PATH="$PROJECT_PATH/.venv/bin/python"

# Cambiar al directorio del proyecto
cd "$PROJECT_PATH"

# Ejecutar la sincronización
echo "$(date): Iniciando sincronización de documentos..."
$VENV_PATH manage.py sync_documents

echo "$(date): Sincronización completada."