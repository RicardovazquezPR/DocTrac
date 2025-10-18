from django.core.management.base import BaseCommand
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Configura el tipo de uso del sistema (personal o empresa)'

    def add_arguments(self, parser):
        parser.add_argument(
            'usage_type',
            choices=['personal', 'empresa'],
            help='Tipo de uso: personal o empresa'
        )

    def handle(self, *args, **options):
        usage_type = options['usage_type']
        
        settings_file = os.path.join(settings.BASE_DIR, 'doctrac', 'settings.py')
        
        # Leer el archivo actual
        with open(settings_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Reemplazar la configuración
        old_line = f"SYSTEM_USAGE_TYPE = '{settings.SYSTEM_USAGE_TYPE if hasattr(settings, 'SYSTEM_USAGE_TYPE') else 'personal'}'"
        new_line = f"SYSTEM_USAGE_TYPE = '{usage_type}'"
        
        if old_line in content:
            content = content.replace(old_line, new_line)
        else:
            # Si no existe, buscamos dónde agregarlo
            if "SYSTEM_USAGE_TYPE" not in content:
                # Agregar después de las carpetas de monitoreo
                insert_after = "os.makedirs(MAIN_FOLDER, exist_ok=True)"
                if insert_after in content:
                    content = content.replace(
                        insert_after,
                        f"{insert_after}\n\n# Configuración de uso del sistema\nSYSTEM_USAGE_TYPE = '{usage_type}'"
                    )
        
        # Escribir el archivo actualizado
        with open(settings_file, 'w', encoding='utf-8') as f:
            f.write(content)
        
        self.stdout.write(
            self.style.SUCCESS(f'✅ Configuración actualizada a: {usage_type}')
        )
        
        # Mostrar información sobre el cambio
        config = settings.USAGE_CONFIG.get(usage_type, {})
        person_label = config.get('person_label', 'Persona')
        
        self.stdout.write(f"📋 Etiqueta de personas/departamentos: {person_label}")
        
        if usage_type == 'empresa':
            self.stdout.write("🏢 Modo empresa activado:")
            self.stdout.write("  - Se mostrarán departamentos en lugar de personas")
            self.stdout.write("  - Se pueden crear departamentos internos")
            self.stdout.write("  - Las empresas externas siguen disponibles")
        else:
            self.stdout.write("👤 Modo personal activado:")
            self.stdout.write("  - Se mostrarán personas y empresas")
            self.stdout.write("  - Ideal para uso personal o freelance")
        
        self.stdout.write("\n🔄 Reinicia el servidor para aplicar los cambios")