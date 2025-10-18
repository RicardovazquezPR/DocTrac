from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.forms import ModelForm
from django.core.management import call_command
from django.conf import settings
from pathlib import Path
import os
from documents.models import Entity, Category, DocumentType

class EntityForm(ModelForm):
    class Meta:
        model = Entity
        fields = ['name', 'value', 'description', 'is_company', 'is_department', 'auto_create_folder']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Generar valor automáticamente basado en el nombre si está vacío
        if not self.instance.pk and not self.initial.get('value'):
            self.fields['value'].widget.attrs['placeholder'] = 'Se genera automáticamente del nombre'

class CategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'value', 'description', 'is_active', 'applies_to_all', 'applicable_entities']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['applicable_entities'].queryset = Entity.objects.all().order_by('name')
        self.fields['applicable_entities'].widget.attrs.update({
            'class': 'form-control',
            'size': '10',
            'style': 'height: auto;'
        })
        # Generar valor automáticamente basado en el nombre si está vacío
        if not self.instance.pk and not self.initial.get('value'):
            self.fields['value'].widget.attrs['placeholder'] = 'Se genera automáticamente del nombre'

class DocumentTypeForm(ModelForm):
    class Meta:
        model = DocumentType
        fields = ['name', 'value', 'category', 'description', 'is_active']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.filter(is_active=True).order_by('name')
        # Generar valor automáticamente basado en el nombre si está vacío
        if not self.instance.pk and not self.initial.get('value'):
            self.fields['value'].widget.attrs['placeholder'] = 'Se genera automáticamente del nombre'

@login_required
def administration_dashboard(request):
    """Dashboard de administración para entidades, categorías y tipos de documentos"""
    from documents.models import Document
    
    entities = Entity.objects.all().order_by('name')
    categories = Category.objects.all().order_by('name')
    document_types = DocumentType.objects.all().order_by('name')
    documents = Document.objects.all()
    
    # Estadísticas
    context = {
        'entities': entities,
        'categories': categories,
        'document_types': document_types,
        'stats': {
            'total_entities': entities.count(),
            'total_categories': categories.count(),
            'total_documents': documents.count(),
            'persons_with_folders': entities.filter(folder_path__isnull=False, folder_path__gt='').count(),
            'total_document_types': document_types.count(),
            'active_categories': categories.filter(is_active=True).count(),
            'active_document_types': document_types.filter(is_active=True).count(),
        }
    }
    
    return render(request, 'documents/administration.html', context)

@login_required
def create_person(request):
    """Crear nueva persona/empresa/departamento"""
    if request.method == 'POST':
        form = EntityForm(request.POST)
        if form.is_valid():
            entity = form.save()
            messages.success(request, f'Entidad "{entity.name}" creada exitosamente.')
            
            # Si se activó la creación automática de carpetas, crearlas
            if entity.auto_create_folder:
                entity.create_folder_structure()
                messages.success(request, f'Carpeta creada en: {entity.folder_path}')
            
            # Redirigir a la página de gestión de entidades
            return redirect('admin_manage_entities')
    
    form = EntityForm()
    return render(request, 'documents/forms/entity_form.html', {'form': form})

@login_required
def edit_person(request, person_id):
    """Editar persona/empresa/departamento existente"""
    entity = get_object_or_404(Entity, id=person_id)
    
    if request.method == 'POST':
        form = EntityForm(request.POST, instance=entity)
        if form.is_valid():
            old_auto_create = entity.auto_create_folder
            entity = form.save()
            
            # Si se activó la creación automática y no la tenía antes
            if entity.auto_create_folder and not old_auto_create:
                entity.create_folder_structure()
                messages.success(request, f'Carpeta creada en: {entity.folder_path}')
            
            messages.success(request, f'Entidad "{entity.name}" actualizada exitosamente.')
            # Redirigir a la página de gestión de entidades
            return redirect('admin_manage_entities')
    
    form = EntityForm(instance=entity)
    return render(request, 'documents/forms/entity_form.html', {'form': form, 'entity': entity})

@login_required
def create_category(request):
    """Crear nueva categoría"""
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save()
            messages.success(request, f'Categoría "{category.name}" creada exitosamente.')
            
            # Crear carpetas en las personas aplicables
            category.create_category_folders()
            messages.success(request, 'Carpetas de categoría creadas en las personas aplicables.')
            
            # Redirigir a la página de gestión de categorías
            return redirect('admin_manage_categories')
    
    form = CategoryForm()
    return render(request, 'documents/forms/category_form.html', {'form': form})

@login_required
def edit_category(request, category_id):
    """Editar categoría existente"""
    category = get_object_or_404(Category, id=category_id)
    
    if request.method == 'POST':
        form = CategoryForm(request.POST, instance=category)
        if form.is_valid():
            category = form.save()
            
            # Actualizar carpetas según nuevas configuraciones
            category.update_person_folders()
            
            messages.success(request, f'Categoría "{category.name}" actualizada exitosamente.')
            messages.success(request, 'Carpetas actualizadas según nueva configuración.')
            
            # Redirigir a la página de gestión de categorías
            return redirect('admin_manage_categories')
    
    form = CategoryForm(instance=category)
    return render(request, 'documents/forms/category_form.html', {'form': form, 'category': category})

@login_required
def manage_persons(request):
    """Vista para gestionar todas las personas"""
    entities = Entity.objects.all().order_by('name')
    
    # Estadísticas
    stats = {
        'total_entities': entities.count(),
        'physical_entities': entities.filter(is_company=False).count(),
        'moral_entities': entities.filter(is_company=True).count(),
        'with_folders': entities.exclude(folder_path__isnull=True).exclude(folder_path='').count(),
    }
    
    context = {
        'entities': entities,
        'stats': stats,
    }
    return render(request, 'documents/manage_persons.html', context)


def manage_categories(request):
    """Vista para gestionar todas las categorías"""
    categories = Category.objects.all().order_by('name')
    
    # Estadísticas
    stats = {
        'total_categories': categories.count(),
        'active_categories': categories.filter(is_active=True).count(),
        'global_categories': categories.filter(applies_to_all=True).count(),
        'specific_categories': categories.filter(applies_to_all=False).count(),
    }
    
    context = {
        'categories': categories,
        'stats': stats,
    }
    return render(request, 'documents/manage_categories.html', context)


def rebuild_folders(request):
    """Vista para reconstruir todas las carpetas del sistema"""
    if request.method == 'POST':
        try:
            # Usar el comando de gestión para reconstruir carpetas
            from django.core.management import call_command
            from io import StringIO
            
            # Capturar la salida del comando
            output = StringIO()
            call_command('manage_folders', action='create-all', stdout=output)
            
            messages.success(request, f'Carpetas reconstruidas exitosamente: {output.getvalue()}')
        except Exception as e:
            messages.error(request, f'Error al reconstruir carpetas: {str(e)}')
    
    return redirect('documents:administration_dashboard')


# ========================
# VISTAS PARA TIPOS DE DOCUMENTOS
# ========================

@login_required
def create_document_type(request):
    """Vista para crear un nuevo tipo de documento"""
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST)
        if form.is_valid():
            document_type = form.save()
            messages.success(request, f'Tipo de documento "{document_type.name}" creado exitosamente.')
            return redirect('admin_manage_document_types')
    else:
        form = DocumentTypeForm()
    
    return render(request, 'documents/forms/document_type_form.html', {'form': form})

@login_required
def edit_document_type(request, doc_type_id):
    """Vista para editar un tipo de documento existente"""
    document_type = get_object_or_404(DocumentType, id=doc_type_id)
    
    if request.method == 'POST':
        form = DocumentTypeForm(request.POST, instance=document_type)
        if form.is_valid():
            form.save()
            messages.success(request, f'Tipo de documento "{document_type.name}" actualizado exitosamente.')
            return redirect('admin_manage_document_types')
    else:
        form = DocumentTypeForm(instance=document_type)
    
    return render(request, 'documents/forms/document_type_form.html', {'form': form, 'document_type': document_type})

@login_required
def delete_document_type(request, doc_type_id):
    """Vista para eliminar un tipo de documento"""
    document_type = get_object_or_404(DocumentType, id=doc_type_id)
    
    if request.method == 'POST':
        doc_type_name = document_type.name
        document_type.delete()
        messages.success(request, f'Tipo de documento "{doc_type_name}" eliminado exitosamente.')
        return JsonResponse({'success': True})
    
    return JsonResponse({'success': False, 'error': 'Método no permitido'})

@login_required
def manage_document_types(request):
    """Vista para gestionar todos los tipos de documentos"""
    document_types = DocumentType.objects.all().order_by('category__name', 'name')
    
    # Estadísticas
    stats = {
        'total_document_types': document_types.count(),
        'active_document_types': document_types.filter(is_active=True).count(),
        'inactive_document_types': document_types.filter(is_active=False).count(),
        'categories_with_types': Category.objects.filter(document_types__isnull=False).distinct().count(),
    }
    
    context = {
        'document_types': document_types,
        'stats': stats,
    }
    return render(request, 'documents/manage_document_types.html', context)

@login_required
def sync_workfolder(request):
    """Vista para sincronizar manualmente los documentos de la carpeta WorkFolder"""
    if request.method == 'POST':
        try:
            # Verificar que la carpeta WorkFolder existe
            monitored_folder = Path(settings.MONITORED_FOLDER)
            if not monitored_folder.exists():
                messages.error(request, f'La carpeta WorkFolder no existe en: {monitored_folder}')
                return JsonResponse({'success': False, 'error': 'Carpeta no encontrada'})
            
            # Contar archivos PDF pendientes antes de la sincronización
            pdf_files = list(monitored_folder.glob('*.pdf'))
            pending_count = len(pdf_files)
            
            if pending_count == 0:
                messages.info(request, 'No hay documentos PDF pendientes en la carpeta WorkFolder.')
                return JsonResponse({
                    'success': True, 
                    'message': 'No hay documentos pendientes',
                    'processed': 0,
                    'pending': 0
                })
            
            # Ejecutar el comando de sincronización
            call_command('sync_documents')
            
            # Verificar cuántos archivos quedaron después de la sincronización
            remaining_pdf_files = list(monitored_folder.glob('*.pdf'))
            remaining_count = len(remaining_pdf_files)
            processed_count = pending_count - remaining_count
            
            if processed_count > 0:
                messages.success(request, 
                    f'✅ Sincronización completada: {processed_count} documentos procesados, '
                    f'{remaining_count} documentos pendientes.'
                )
            else:
                messages.warning(request, 
                    'Sincronización ejecutada pero no se procesaron nuevos documentos. '
                    'Posiblemente ya estaban en el sistema.'
                )
            
            return JsonResponse({
                'success': True,
                'message': 'Sincronización completada',
                'processed': processed_count,
                'pending': remaining_count
            })
            
        except Exception as e:
            messages.error(request, f'Error durante la sincronización: {str(e)}')
            return JsonResponse({'success': False, 'error': str(e)})
    
    # Si es GET, mostrar información sobre la carpeta WorkFolder
    try:
        monitored_folder = Path(settings.MONITORED_FOLDER)
        if monitored_folder.exists():
            pdf_files = list(monitored_folder.glob('*.pdf'))
            pending_count = len(pdf_files)
            
            # Información sobre la carpeta processed
            processed_folder = monitored_folder / 'processed'
            processed_count = 0
            if processed_folder.exists():
                processed_files = list(processed_folder.glob('*.*'))
                processed_count = len(processed_files)
            
            context = {
                'monitored_folder': str(monitored_folder),
                'pending_count': pending_count,
                'processed_count': processed_count,
                'folder_exists': True,
                'pending_files': [f.name for f in pdf_files[:10]]  # Mostrar hasta 10 archivos
            }
        else:
            context = {
                'monitored_folder': str(monitored_folder),
                'folder_exists': False,
                'pending_count': 0,
                'processed_count': 0
            }
    except Exception as e:
        messages.error(request, f'Error al acceder a la carpeta WorkFolder: {str(e)}')
        context = {
            'error': str(e)
        }
    
    return render(request, 'documents/sync_workfolder.html', context)