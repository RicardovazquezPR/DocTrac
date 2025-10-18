import os
import shutil
from datetime import datetime
from pathlib import Path
from django.core.management.base import BaseCommand
from django.conf import settings
from documents.models import Document, Category
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Sincroniza documentos desde la carpeta de monitoreo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Muestra qué archivos se procesarían sin realizar cambios',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']
        
        monitored_folder = Path(settings.MONITORED_FOLDER)
        
        if not monitored_folder.exists():
            self.stdout.write(
                self.style.ERROR(f'La carpeta de monitoreo no existe: {monitored_folder}')
            )
            return
        
        # Obtener archivos PDF en la carpeta de monitoreo
        pdf_files = list(monitored_folder.glob('*.pdf'))
        
        if not pdf_files:
            self.stdout.write(
                self.style.SUCCESS('No se encontraron nuevos documentos PDF en la carpeta de monitoreo.')
            )
            return
        
        # Obtener categoría por defecto para documentos escaneados
        default_category, created = Category.objects.get_or_create(
            name='Documentos Escaneados',
            defaults={'description': 'Documentos importados automáticamente desde la carpeta de monitoreo'}
        )
        
        if created:
            self.stdout.write(
                self.style.SUCCESS(f'Creada categoría: {default_category.name}')
            )
        
        # Obtener el primer usuario como propietario por defecto (podríamos mejorarlo)
        default_user = User.objects.first()
        if not default_user:
            self.stdout.write(
                self.style.ERROR('No se encontraron usuarios en el sistema. Crea al menos un usuario.')
            )
            return
        
        processed_count = 0
        
        for pdf_file in pdf_files:
            # Verificar si el documento ya existe en la base de datos
            existing_doc = Document.objects.filter(
                original_filename=pdf_file.name
            ).first()
            
            if existing_doc:
                self.stdout.write(
                    self.style.WARNING(f'Documento ya existe: {pdf_file.name}')
                )
                continue
            
            if dry_run:
                self.stdout.write(
                    self.style.SUCCESS(f'[DRY RUN] Procesaría: {pdf_file.name}')
                )
                processed_count += 1
                continue
            
            try:
                # Crear el documento en la base de datos
                document = Document.objects.create(
                    title=pdf_file.stem,  # Nombre sin extensión
                    notes=f'Documento escaneado importado automáticamente el {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                    category=default_category,
                    created_by=default_user,
                    original_filename=pdf_file.name,
                    imported_from_folder=True,
                    status='pending'
                )
                
                # Copiar el archivo a la carpeta de media de Django
                media_path = Path(settings.MEDIA_ROOT) / 'documents'
                media_path.mkdir(parents=True, exist_ok=True)
                
                # Generar nombre único para evitar conflictos
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                new_filename = f"{document.id}_{timestamp}_{pdf_file.name}"
                destination = media_path / new_filename
                
                # Copiar el archivo
                shutil.copy2(pdf_file, destination)
                
                # Actualizar el campo file del documento
                document.file = f'documents/{new_filename}'
                document.save()
                
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Procesado: {pdf_file.name} -> ID: {document.id}')
                )
                
                processed_count += 1
                
                # Opcional: Mover el archivo original a una carpeta de procesados
                processed_folder = monitored_folder / 'processed'
                processed_folder.mkdir(exist_ok=True)
                
                processed_file = processed_folder / f"{timestamp}_{pdf_file.name}"
                shutil.move(pdf_file, processed_file)
                
                self.stdout.write(
                    self.style.SUCCESS(f'📁 Movido a procesados: {processed_file.name}')
                )
                
            except Exception as e:
                self.stdout.write(
                    self.style.ERROR(f'❌ Error procesando {pdf_file.name}: {str(e)}')
                )
        
        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(f'[DRY RUN] Se procesarían {processed_count} documentos')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(f'✅ Procesados {processed_count} documentos nuevos')
            )