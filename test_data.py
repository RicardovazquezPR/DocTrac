#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctrac.settings')
django.setup()

from documents.models import Entity, Category, DocumentType

def create_test_data():
    # Crear una entidad de prueba
    entity, created = Entity.objects.get_or_create(
        name='Empresa ABC S.A. de C.V.',
        defaults={
            'value': 'ABC',
            'description': 'Empresa de servicios administrativos',
            'is_company': True,
            'is_department': False
        }
    )

    # Crear una categoría de prueba
    category, created = Category.objects.get_or_create(
        name='Documentos Fiscales',
        defaults={
            'value': 'FIS',
            'is_active': True
        }
    )

    # Crear un tipo de documento de prueba
    doc_type, created = DocumentType.objects.get_or_create(
        name='Factura de Compra',
        category=category,
        defaults={
            'value': 'INV',
            'is_active': True
        }
    )

    print(f'Entidad: {entity.name} -> {entity.value}')
    print(f'Categoría: {category.name} -> {category.value}')
    print(f'Tipo documento: {doc_type.name} -> {doc_type.value}')
    print('Datos de prueba creados exitosamente!')

if __name__ == '__main__':
    create_test_data()