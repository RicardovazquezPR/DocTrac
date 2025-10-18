from django.core.management.base import BaseCommand
from documents.models import Entity
from django.conf import settings

class Command(BaseCommand):
    help = 'Crea datos de ejemplo según el tipo de uso configurado'

    def handle(self, *args, **options):
        usage_type = getattr(settings, 'SYSTEM_USAGE_TYPE', 'personal')
        
        if usage_type == 'empresa':
            self.stdout.write("🏢 Creando departamentos de ejemplo...")
            
            departamentos = [
                {'name': 'Recursos Humanos', 'description': 'Departamento de gestión de personal'},
                {'name': 'Finanzas', 'description': 'Departamento financiero y contable'},
                {'name': 'Ventas', 'description': 'Departamento de ventas y comercial'},
                {'name': 'Marketing', 'description': 'Departamento de marketing y publicidad'},
                {'name': 'Operaciones', 'description': 'Departamento de operaciones y logística'},
                {'name': 'IT / Sistemas', 'description': 'Departamento de tecnología e informática'},
                {'name': 'Legal', 'description': 'Departamento jurídico y legal'},
                {'name': 'Administración', 'description': 'Departamento administrativo general'},
            ]
            
            for dept_data in departamentos:
                dept, created = Entity.objects.get_or_create(
                    name=dept_data['name'],
                    is_department=True,
                    defaults={
                        'is_company': False,
                        'address': dept_data['description']
                    }
                )
                if created:
                    self.stdout.write(f"  ✅ Creado: {dept_data['name']}")
                else:
                    self.stdout.write(f"  ℹ️  Ya existe: {dept_data['name']}")
            
            # Crear algunas empresas externas de ejemplo
            empresas_externas = [
                'Proveedor ABC S.A.',
                'Cliente Corporativo XYZ',
                'Banco Nacional',
                'Consultoría Externa',
            ]
            
            for empresa in empresas_externas:
                emp, created = Entity.objects.get_or_create(
                    name=empresa,
                    is_company=True,
                    defaults={
                        'is_department': False,
                    }
                )
                if created:
                    self.stdout.write(f"  🏢 Creada empresa: {empresa}")
        
        else:  # personal
            self.stdout.write("👤 Creando personas y empresas de ejemplo...")
            
            personas = [
                'Juan Pérez',
                'María García',
                'Carlos López',
                'Ana Martínez',
            ]
            
            for persona in personas:
                per, created = Entity.objects.get_or_create(
                    name=persona,
                    is_company=False,
                    defaults={
                        'is_department': False,
                    }
                )
                if created:
                    self.stdout.write(f"  👤 Creada persona: {persona}")
            
            empresas = [
                'Empresa ABC',
                'Corporación XYZ', 
                'Servicios Generales S.A.',
                'Consultoría Profesional',
            ]
            
            for empresa in empresas:
                emp, created = Entity.objects.get_or_create(
                    name=empresa,
                    is_company=True,
                    defaults={
                        'is_department': False,
                    }
                )
                if created:
                    self.stdout.write(f"  🏢 Creada empresa: {empresa}")
        
        self.stdout.write(
            self.style.SUCCESS(f"\n✅ Datos de ejemplo creados para modo: {usage_type}")
        )