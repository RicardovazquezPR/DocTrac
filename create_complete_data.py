#!/usr/bin/env python
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'doctrac.settings')
django.setup()

from documents.models import Entity, Category, DocumentType

def create_comprehensive_test_data():
    """Crea un conjunto completo de datos para demostrar el sistema"""
    
    print("📋 CREANDO DATOS COMPLETOS DE EJEMPLO")
    print("=" * 45)
    print()
    
    # Crear múltiples entidades
    entities_data = [
        {"name": "Empresa ABC S.A. de C.V.", "value": "ABC", "is_company": True},
        {"name": "XYZ Corporation", "value": "XYZ", "is_company": True},
        {"name": "Juan Pérez", "value": "JPZ", "is_company": False},
        {"name": "María González", "value": "MGZ", "is_company": False},
        {"name": "Recursos Humanos - ABC", "value": "RH", "is_company": True, "is_department": True},
    ]
    
    # Crear múltiples categorías
    categories_data = [
        {"name": "Documentos Fiscales", "value": "FIS"},
        {"name": "Recursos Humanos", "value": "RH"},
        {"name": "Contabilidad", "value": "CON"},
        {"name": "Legales", "value": "LEG"},
        {"name": "Administrativos", "value": "ADM"},
    ]
    
    # Crear múltiples tipos de documento
    doc_types_data = [
        # Fiscales
        {"name": "Factura de Compra", "value": "INV", "category_value": "FIS"},
        {"name": "Factura de Venta", "value": "FVE", "category_value": "FIS"},
        {"name": "Recibo de Honorarios", "value": "HON", "category_value": "FIS"},
        
        # Recursos Humanos
        {"name": "Contrato Laboral", "value": "CNT", "category_value": "RH"},
        {"name": "Nómina", "value": "NOM", "category_value": "RH"},
        {"name": "Expediente Personal", "value": "EXP", "category_value": "RH"},
        
        # Contabilidad
        {"name": "Estado de Cuenta", "value": "EDC", "category_value": "CON"},
        {"name": "Conciliación Bancaria", "value": "CBN", "category_value": "CON"},
        
        # Legales
        {"name": "Acta Constitutiva", "value": "ACT", "category_value": "LEG"},
        {"name": "Poder Notarial", "value": "POD", "category_value": "LEG"},
    ]
    
    print("🏢 Creando entidades...")
    for entity_data in entities_data:
        entity, created = Entity.objects.get_or_create(
            name=entity_data["name"],
            defaults={
                'value': entity_data["value"],
                'description': f'Entidad {entity_data["name"]}',
                'is_company': entity_data["is_company"],
                'is_department': entity_data.get("is_department", False)
            }
        )
        status = "✅ Creada" if created else "🔄 Ya existe"
        print(f"   {status}: {entity.name} -> {entity.value}")
    
    print("\n📂 Creando categorías...")
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            name=cat_data["name"],
            defaults={
                'value': cat_data["value"],
                'is_active': True
            }
        )
        status = "✅ Creada" if created else "🔄 Ya existe"
        print(f"   {status}: {category.name} -> {category.value}")
    
    print("\n📄 Creando tipos de documento...")
    for doc_data in doc_types_data:
        category = Category.objects.get(value=doc_data["category_value"])
        doc_type, created = DocumentType.objects.get_or_create(
            name=doc_data["name"],
            category=category,
            defaults={
                'value': doc_data["value"],
                'is_active': True
            }
        )
        status = "✅ Creado" if created else "🔄 Ya existe"
        print(f"   {status}: {doc_type.name} -> {doc_type.value} ({category.value})")
    
    print("\n📊 RESUMEN DEL SISTEMA:")
    print(f"   🏢 Entidades: {Entity.objects.count()}")
    print(f"   📂 Categorías: {Category.objects.count()}")
    print(f"   📄 Tipos de documento: {DocumentType.objects.count()}")
    
    print("\n💡 EJEMPLOS DE NOMBRES PDF GENERADOS:")
    examples = [
        ("ABC", "FIS", "INV", "ABC_FIS_INV_20251014.pdf"),
        ("XYZ", "RH", "CNT", "XYZ_RH_CNT_20251014.pdf"),
        ("JPZ", "LEG", "POD", "JPZ_LEG_POD_20251014.pdf"),
        ("MGZ", "CON", "EDC", "MGZ_CON_EDC_20251014.pdf"),
        ("RH", "RH", "EXP", "RH_RH_EXP_20251014.pdf"),
    ]
    
    for entity_val, cat_val, doc_val, filename in examples:
        print(f"   📎 {filename}")
    
    print(f"\n✅ Sistema configurado con datos completos!")

if __name__ == '__main__':
    create_comprehensive_test_data()