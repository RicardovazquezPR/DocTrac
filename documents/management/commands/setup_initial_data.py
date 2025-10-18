from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from documents.models import Category, DocumentType, Entity

User = get_user_model()

class Command(BaseCommand):
    help = 'Crear datos iniciales para el sistema DocTrac'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Creando datos iniciales...'))
        
        # Crear superusuario admin si no existe
        if not User.objects.filter(username='admin').exists():
            admin_user = User.objects.create_superuser(
                username='admin',
                email='admin@doctrac.com',
                password='admin123',
                first_name='Administrador',
                last_name='Sistema',
                role='admin'
            )
            self.stdout.write(self.style.SUCCESS(f'Superusuario creado: {admin_user.username}'))
        else:
            self.stdout.write(self.style.WARNING('El usuario admin ya existe'))
        
        # Crear usuarios de ejemplo
        users_data = [
            {
                'username': 'manager1',
                'email': 'manager@doctrac.com',
                'password': 'manager123',
                'first_name': 'María',
                'last_name': 'González',
                'role': 'manager',
                'department': 'Administración'
            },
            {
                'username': 'user1',
                'email': 'user1@doctrac.com',
                'password': 'user123',
                'first_name': 'Carlos',
                'last_name': 'Rodríguez',
                'role': 'user',
                'department': 'Contabilidad'
            },
            {
                'username': 'user2',
                'email': 'user2@doctrac.com',
                'password': 'user123',
                'first_name': 'Ana',
                'last_name': 'Martínez',
                'role': 'user',
                'department': 'Recursos Humanos'
            }
        ]
        
        for user_data in users_data:
            username = user_data['username']
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(**user_data)
                self.stdout.write(self.style.SUCCESS(f'Usuario creado: {user.username} - {user.get_role_display()}'))
            else:
                self.stdout.write(self.style.WARNING(f'El usuario {username} ya existe'))
        
        # Crear categorías
        categories_data = [
            {'name': 'Facturas', 'description': 'Facturas de proveedores y clientes'},
            {'name': 'Contratos', 'description': 'Contratos y acuerdos legales'},
            {'name': 'Recursos Humanos', 'description': 'Documentos de personal y empleados'},
            {'name': 'Finanzas', 'description': 'Estados financieros y reportes contables'},
            {'name': 'Legal', 'description': 'Documentos legales y jurídicos'},
            {'name': 'Administrativo', 'description': 'Documentos administrativos generales'}
        ]
        
        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={'description': cat_data['description']}
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Categoría creada: {category.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'La categoría {category.name} ya existe'))
        
        # Crear tipos de documentos
        document_types_data = [
            # Facturas
            {'name': 'Factura de Venta', 'category': 'Facturas'},
            {'name': 'Factura de Compra', 'category': 'Facturas'},
            {'name': 'Nota de Crédito', 'category': 'Facturas'},
            {'name': 'Nota de Débito', 'category': 'Facturas'},
            
            # Contratos
            {'name': 'Contrato de Servicios', 'category': 'Contratos'},
            {'name': 'Contrato de Compraventa', 'category': 'Contratos'},
            {'name': 'Contrato de Arrendamiento', 'category': 'Contratos'},
            {'name': 'Convenio de Colaboración', 'category': 'Contratos'},
            
            # Recursos Humanos
            {'name': 'Contrato Laboral', 'category': 'Recursos Humanos'},
            {'name': 'Renuncia', 'category': 'Recursos Humanos'},
            {'name': 'Solicitud de Vacaciones', 'category': 'Recursos Humanos'},
            {'name': 'Evaluación de Desempeño', 'category': 'Recursos Humanos'},
            
            # Finanzas
            {'name': 'Estado de Cuenta', 'category': 'Finanzas'},
            {'name': 'Conciliación Bancaria', 'category': 'Finanzas'},
            {'name': 'Reporte Financiero', 'category': 'Finanzas'},
            {'name': 'Presupuesto', 'category': 'Finanzas'},
            
            # Legal
            {'name': 'Escritura Pública', 'category': 'Legal'},
            {'name': 'Poder Notarial', 'category': 'Legal'},
            {'name': 'Demanda', 'category': 'Legal'},
            {'name': 'Sentencia', 'category': 'Legal'},
            
            # Administrativo
            {'name': 'Oficio', 'category': 'Administrativo'},
            {'name': 'Memorándum', 'category': 'Administrativo'},
            {'name': 'Circular', 'category': 'Administrativo'},
            {'name': 'Acta', 'category': 'Administrativo'}
        ]
        
        for doc_type_data in document_types_data:
            try:
                category = Category.objects.get(name=doc_type_data['category'])
                doc_type, created = DocumentType.objects.get_or_create(
                    name=doc_type_data['name'],
                    category=category
                )
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Tipo de documento creado: {doc_type.name}'))
                else:
                    self.stdout.write(self.style.WARNING(f'El tipo de documento {doc_type.name} ya existe'))
            except Category.DoesNotExist:
                self.stdout.write(self.style.ERROR(f'Categoría no encontrada: {doc_type_data["category"]}'))
        
        # Crear personas/empresas de ejemplo
        persons_data = [
            # Personas
            {
                'name': 'Juan Pérez García',
                'is_company': False,
                'tax_id': 'PEGJ850315ABC',
                'phone': '555-1234',
                'email': 'juan.perez@email.com'
            },
            {
                'name': 'María Elena Rodríguez',
                'is_company': False,
                'tax_id': 'ROME901020DEF',
                'phone': '555-5678',
                'email': 'maria.rodriguez@email.com'
            },
            {
                'name': 'Carlos Alberto Martínez',
                'is_company': False,
                'tax_id': 'MACL880715GHI',
                'phone': '555-9012',
                'email': 'carlos.martinez@email.com'
            },
            
            # Empresas
            {
                'name': 'Tecnología y Servicios S.A. de C.V.',
                'is_company': True,
                'tax_id': 'TSE120615JKL',
                'phone': '555-3456',
                'email': 'contacto@tecnologiayservicios.com',
                'address': 'Av. Reforma 123, Col. Centro, CDMX'
            },
            {
                'name': 'Consultoría Integral MX',
                'is_company': True,
                'tax_id': 'CIM180920MNO',
                'phone': '555-7890',
                'email': 'info@consultoriaintegral.mx',
                'address': 'Blvd. Insurgentes 456, Col. Roma Norte, CDMX'
            },
            {
                'name': 'Distribuidora Nacional S.A.',
                'is_company': True,
                'tax_id': 'DNS150310PQR',
                'phone': '555-2468',
                'email': 'ventas@distribuidoranacional.com',
                'address': 'Calz. Tlalpan 789, Col. Del Valle, CDMX'
            },
            {
                'name': 'Servicios Profesionales Beta',
                'is_company': True,
                'tax_id': 'SPB190825STU',
                'phone': '555-1357',
                'email': 'contacto@serviciosbeta.com',
                'address': 'Av. Universidad 321, Col. Narvarte, CDMX'
            }
        ]
        
        for entity_data in persons_data:
            entity, created = Entity.objects.get_or_create(
                name=entity_data['name'],
                defaults=entity_data
            )
            if created:
                tipo = 'Empresa' if entity.is_company else 'Entidad'
                self.stdout.write(self.style.SUCCESS(f'{tipo} creada: {entity.name}'))
            else:
                self.stdout.write(self.style.WARNING(f'La entidad {entity.name} ya existe'))
        
        self.stdout.write(self.style.SUCCESS('\n=== DATOS INICIALES CREADOS ==='))
        self.stdout.write(self.style.SUCCESS('Usuarios de acceso:'))
        self.stdout.write(self.style.SUCCESS('  Admin: admin / admin123'))
        self.stdout.write(self.style.SUCCESS('  Manager: manager1 / manager123'))
        self.stdout.write(self.style.SUCCESS('  Usuario: user1 / user123'))
        self.stdout.write(self.style.SUCCESS('  Usuario: user2 / user123'))
        self.stdout.write(self.style.SUCCESS('\nPuedes acceder al admin en: http://localhost:8000/admin/'))
        self.stdout.write(self.style.SUCCESS('Y al sistema en: http://localhost:8000/'))