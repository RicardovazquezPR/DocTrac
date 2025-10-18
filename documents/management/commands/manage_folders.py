from django.core.management.base import BaseCommand
from documents.models import Entity, Category
from django.conf import settings
import os

class Command(BaseCommand):
    help = 'Administra las carpetas del sistema de documentos'

    def add_arguments(self, parser):
        parser.add_argument(
            '--action',
            choices=['create-all', 'create-person', 'create-categories', 'list-structure'],
            default='create-all',
            help='Acción a realizar'
        )
        parser.add_argument(
            '--person-id',
            type=int,
            help='ID de la persona para crear carpeta específica'
        )

    def handle(self, *args, **options):
        action = options['action']
        
        self.stdout.write(f"🗂️  Administrador de Carpetas - {action}")
        self.stdout.write("=" * 50)
        
        if action == 'create-all':
            self.create_all_folders()
        elif action == 'create-person':
            person_id = options.get('person_id')
            if person_id:
                self.create_person_folder(person_id)
            else:
                self.stdout.write(self.style.ERROR("Se requiere --person-id"))
        elif action == 'create-categories':
            self.create_category_folders()
        elif action == 'list-structure':
            self.list_folder_structure()
    
    def create_all_folders(self):
        """Crea todas las carpetas del sistema"""
        self.stdout.write("📁 Creando estructura completa de carpetas...")
        
        # Crear carpetas base para todas las personas
        persons = Entity.objects.filter(auto_create_folder=True)
        
        for person in persons:
            self.stdout.write(f"👤 Procesando: {person.name}")
            person.create_folder_structure()
            
        self.stdout.write(f"✅ Carpetas creadas para {persons.count()} personas")
        
        # Crear carpetas de categorías
        self.create_category_folders()
    
    def create_person_folder(self, person_id):
        """Crea carpeta para una persona específica"""
        try:
            entity = Entity.objects.get(id=person_id)
            entity.create_folder_structure()
            self.stdout.write(f"✅ Carpeta creada para: {entity.name}")
        except Entity.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"Persona con ID {person_id} no encontrada"))
    
    def create_category_folders(self):
        """Crea carpetas de categorías en todas las personas aplicables"""
        self.stdout.write("🏷️  Creando carpetas de categorías...")
        
        categories = Category.objects.filter(is_active=True)
        
        for category in categories:
            self.stdout.write(f"📂 Procesando categoría: {category.name}")
            category.create_category_folders()
            
        self.stdout.write(f"✅ Carpetas de categorías procesadas: {categories.count()}")
    
    def list_folder_structure(self):
        """Lista la estructura de carpetas actual"""
        self.stdout.write("📋 ESTRUCTURA ACTUAL DE CARPETAS")
        self.stdout.write("=" * 40)
        
        main_folder = getattr(settings, 'MAIN_FOLDER', None)
        if not main_folder:
            self.stdout.write(self.style.ERROR("MAIN_FOLDER no configurado"))
            return
        
        self.stdout.write(f"📁 Carpeta base: {main_folder}")
        
        persons = Entity.objects.filter(folder_path__isnull=False)
        
        for person in persons:
            self.stdout.write(f"\n👤 {person.name}")
            
            if person.folder_path and os.path.exists(person.folder_path):
                self.stdout.write(f"   📍 {person.folder_path}")
                
                # Listar subcarpetas
                try:
                    subdirs = [d for d in os.listdir(person.folder_path) 
                              if os.path.isdir(os.path.join(person.folder_path, d))]
                    
                    if subdirs:
                        for subdir in sorted(subdirs):
                            self.stdout.write(f"   └── 📂 {subdir}")
                    else:
                        self.stdout.write("   └── (sin subcarpetas)")
                        
                except Exception as e:
                    self.stdout.write(f"   └── ❌ Error listando: {e}")
            else:
                self.stdout.write("   └── ❌ Carpeta no existe")
        
        # Estadísticas
        total_persons = Entity.objects.count()
        persons_with_folders = persons.count()
        active_categories = Category.objects.filter(is_active=True).count()
        
        self.stdout.write(f"\n📊 ESTADÍSTICAS:")
        self.stdout.write(f"   👥 Total personas: {total_persons}")
        self.stdout.write(f"   📁 Con carpetas: {persons_with_folders}")
        self.stdout.write(f"   🏷️  Categorías activas: {active_categories}")