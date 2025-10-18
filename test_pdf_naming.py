#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctrac.settings')
django.setup()

from documents.models import Entity, Category, DocumentType
from datetime import datetime

def generate_pdf_filename(entity_value, category_value, doc_type_value, date=None, additional_info=""):
    """
    Genera un nombre de archivo PDF usando los valores de entidad, categoría y tipo de documento.
    
    Formato: {entity_value}_{category_value}_{doc_type_value}_{fecha}_{info_adicional}.pdf
    
    Args:
        entity_value (str): Valor de la entidad
        category_value (str): Valor de la categoría  
        doc_type_value (str): Valor del tipo de documento
        date (datetime, optional): Fecha del documento. Si no se proporciona, usa la fecha actual
        additional_info (str, optional): Información adicional para el archivo
    
    Returns:
        str: Nombre del archivo PDF generado
    """
    if date is None:
        date = datetime.now()
    
    # Formatear fecha como YYYYMMDD
    date_str = date.strftime("%Y%m%d")
    
    # Construir nombre base
    filename_parts = [entity_value, category_value, doc_type_value, date_str]
    
    # Agregar información adicional si se proporciona
    if additional_info:
        # Limpiar información adicional (remover espacios y caracteres especiales)
        clean_info = "".join(c for c in additional_info if c.isalnum() or c in ('_', '-')).strip()
        if clean_info:
            filename_parts.append(clean_info)
    
    # Unir todas las partes con guiones bajos
    filename = "_".join(filename_parts) + ".pdf"
    
    return filename

def test_pdf_naming():
    """Prueba la generación de nombres de archivos PDF con datos reales"""
    
    print("=== PRUEBA DE GENERACIÓN DE NOMBRES PDF ===\n")
    
    # Obtener datos de prueba
    try:
        entity = Entity.objects.get(value='ABC')
        category = Category.objects.get(value='FIS')
        doc_type = DocumentType.objects.get(value='INV')
        
        print(f"📋 Datos de prueba:")
        print(f"   - Entidad: {entity.name} -> {entity.value}")
        print(f"   - Categoría: {category.name} -> {category.value}")
        print(f"   - Tipo Doc: {doc_type.name} -> {doc_type.value}")
        print()
        
        # Generar diferentes ejemplos
        examples = [
            {
                'desc': 'Nombre básico (fecha actual)',
                'params': {
                    'entity_value': entity.value,
                    'category_value': category.value,
                    'doc_type_value': doc_type.value
                }
            },
            {
                'desc': 'Con fecha específica',
                'params': {
                    'entity_value': entity.value,
                    'category_value': category.value,
                    'doc_type_value': doc_type.value,
                    'date': datetime(2024, 12, 15)
                }
            },
            {
                'desc': 'Con información adicional',
                'params': {
                    'entity_value': entity.value,
                    'category_value': category.value,
                    'doc_type_value': doc_type.value,
                    'additional_info': 'PROV001'
                }
            },
            {
                'desc': 'Completo con fecha e info adicional',
                'params': {
                    'entity_value': entity.value,
                    'category_value': category.value,
                    'doc_type_value': doc_type.value,
                    'date': datetime(2024, 11, 30),
                    'additional_info': 'INV_12345'
                }
            }
        ]
        
        print("📄 Ejemplos de nombres generados:")
        for example in examples:
            filename = generate_pdf_filename(**example['params'])
            print(f"   {example['desc']}: {filename}")
        
        print()
        print("✅ Todos los ejemplos generados exitosamente!")
        
        # Mostrar todas las entidades, categorías y tipos disponibles
        print("\n📊 DATOS DISPONIBLES EN EL SISTEMA:")
        
        print("\n🏢 Entidades:")
        for ent in Entity.objects.all():
            print(f"   - {ent.name} -> {ent.value}")
            
        print("\n📂 Categorías:")
        for cat in Category.objects.all():
            print(f"   - {cat.name} -> {cat.value}")
            
        print("\n📄 Tipos de Documento:")
        for dt in DocumentType.objects.all():
            print(f"   - {dt.name} -> {dt.value} (Categoría: {dt.category.name})")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Asegúrate de que los datos de prueba existan en la base de datos.")

if __name__ == '__main__':
    test_pdf_naming()