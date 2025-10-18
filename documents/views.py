from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.http import JsonResponse, HttpResponse, Http404
from django.contrib import messages
from django.db.models import Q
from django.urls import reverse_lazy
from django.forms import ModelForm
from django.conf import settings
from .models import Document, Category, DocumentType, Entity, DocumentHistory
import json
import os
import shutil
from pathlib import Path
from datetime import datetime
import logging

# Configurar logger
logger = logging.getLogger(__name__)

@login_required
def dashboard(request):
    """Vista principal del dashboard con interfaz de 3 columnas"""
    user = request.user
    
    # Filtrar documentos según permisos del usuario
    if user.can_view_all_documents():
        pending_documents = Document.objects.filter(status='pending')
        all_documents = Document.objects.all()
    else:
        pending_documents = Document.objects.filter(
            Q(assigned_users=user) | Q(created_by=user),
            status='pending'
        ).distinct()
        all_documents = Document.objects.filter(
            Q(assigned_users=user) | Q(created_by=user)
        ).distinct()
    
    # Obtener categorías y tipos para los dropdowns
    categories = Category.objects.filter(is_active=True)
    document_types = DocumentType.objects.filter(is_active=True)
    
    # Filtrar personas/departamentos según configuración
    from django.conf import settings
    usage_type = getattr(settings, 'SYSTEM_USAGE_TYPE', 'personal')
    
    if usage_type == 'empresa':
        # En modo empresa, mostrar departamentos primero, luego empresas externas
        entities = Entity.objects.all().order_by('is_department', 'name')
    else:
        # En modo personal, mostrar personas y empresas
        entities = Entity.objects.all().order_by('is_company', 'name')
    
    # Configuración de uso para el template
    usage_config = getattr(settings, 'USAGE_CONFIG', {}).get(usage_type, {})
    
    context = {
        'pending_documents': pending_documents[:20],  # Limitar a 20 para performance
        'categories': categories,
        'document_types': document_types,
        'entities': entities,
        'total_documents': all_documents.count(),
        'pending_count': pending_documents.count(),
        'usage_type': usage_type,
        'person_label': usage_config.get('person_label', 'Persona'),
        'person_help_text': usage_config.get('person_help_text', 'Persona asociada al documento'),
        'show_companies': usage_config.get('show_companies', True),
    }
    
    return render(request, 'documents/dashboard.html', context)

@login_required
def document_detail(request, pk):
    """Vista detalle del documento con preview"""
    user = request.user
    document = get_object_or_404(Document, pk=pk)
    
    # Verificar permisos
    if not user.can_view_all_documents():
        if not (document.assigned_users.filter(id=user.id).exists() or document.created_by == user):
            raise Http404("Documento no encontrado")
    
    # Obtener historial
    history = document.history.all()
    
    context = {
        'document': document,
        'history': history,
    }
    
    return render(request, 'documents/document_detail.html', context)

@login_required
def update_document(request, pk):
    """Actualizar información de documento via AJAX"""
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Método no permitido'})
    
    user = request.user
    document = get_object_or_404(Document, pk=pk)
    
    # Verificar permisos
    if not user.can_view_all_documents():
        if not (document.assigned_users.filter(id=user.id).exists() or document.created_by == user):
            return JsonResponse({'success': False, 'error': 'Sin permisos'})
    
    try:
        data = json.loads(request.body)
        
        # Guardar estado anterior para historial
        previous_status = document.status
        
        # Actualizar campos
        if 'category_id' in data and data['category_id']:
            document.category_id = data['category_id']
        
        if 'document_type_id' in data and data['document_type_id']:
            document.document_type_id = data['document_type_id']
        
        if 'person_id' in data and data['person_id']:
            document.entity_id = data['person_id']
        elif 'entity_id' in data and data['entity_id']:
            document.entity_id = data['entity_id']
        
        if 'document_date' in data and data['document_date']:
            document.document_date = data['document_date']
        
        if 'payment_status' in data:
            document.payment_status = data['payment_status']
        
        if 'status' in data:
            document.status = data['status']
        
        if 'notes' in data:
            document.notes = data['notes']
        
        document.save()
        
        # Crear entrada en historial si cambió el estado
        if 'status' in data and previous_status != document.status:
            DocumentHistory.objects.create(
                document=document,
                previous_status=previous_status,
                new_status=document.status,
                changed_by=user,
                change_reason=data.get('change_reason', 'Actualización desde dashboard')
            )
        
        # Generar nombre estructurado de forma segura
        try:
            structured_name = document.get_structured_name()
        except Exception as name_error:
            print(f"Error generando nombre estructurado: {name_error}")
            structured_name = document.title
        
        return JsonResponse({
            'success': True,
            'message': 'Documento actualizado correctamente',
            'structured_name': structured_name
        })
        
    except Exception as e:
        print(f"Error en update_document: {e}")
        return JsonResponse({'success': False, 'error': f'Error al actualizar: {str(e)}'})

@login_required
def get_document_types_by_category(request):
    """Obtener tipos de documento por categoría (para dropdown dependiente)"""
    category_id = request.GET.get('category_id')
    
    if category_id:
        document_types = DocumentType.objects.filter(
            category_id=category_id, 
            is_active=True
        ).values('id', 'name')
        return JsonResponse({'document_types': list(document_types)})
    
    return JsonResponse({'document_types': []})

class DocumentListView(LoginRequiredMixin, ListView):
    """Vista de lista de documentos"""
    model = Document
    template_name = 'documents/document_list.html'
    context_object_name = 'documents'
    paginate_by = 20
    
    def get_queryset(self):
        user = self.request.user
        
        if user.can_view_all_documents():
            queryset = Document.objects.all()
        else:
            queryset = Document.objects.filter(
                Q(assigned_users=user) | Q(created_by=user)
            ).distinct()
        
        # Filtros de búsqueda
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(title__icontains=search) |
                Q(entity__name__icontains=search) |
                Q(notes__icontains=search)
            )
        
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        category = self.request.GET.get('category')
        if category:
            queryset = queryset.filter(category_id=category)
        
        return queryset.select_related('category', 'document_type', 'entity', 'created_by')

class DocumentCreateView(LoginRequiredMixin, CreateView):
    """Vista para crear nuevo documento"""
    model = Document
    template_name = 'documents/document_form.html'
    fields = ['title', 'file', 'category', 'document_type', 'entity', 'document_date', 'payment_status', 'notes', 'assigned_users']
    success_url = reverse_lazy('documents:dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['entities'] = Entity.objects.all()
        context['users'] = get_user_model().objects.filter(is_active=True)
        return context
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        
        # Guardar el documento primero
        response = super().form_valid(form)
        
        # Copiar el archivo a la carpeta de monitoreo si está configurada
        if hasattr(settings, 'MONITORED_FOLDER') and form.instance.file:
            try:
                self._copy_to_monitored_folder(form.instance)
            except Exception as e:
                messages.warning(
                    self.request, 
                    f'Documento creado, pero no se pudo copiar a la carpeta de monitoreo: {str(e)}'
                )
        
        messages.success(self.request, 'Documento creado exitosamente.')
        return response
    
    def _copy_to_monitored_folder(self, document):
        """Copia el archivo subido a la carpeta de monitoreo"""
        if not document.file:
            return

        monitored_folder = Path(settings.MONITORED_FOLDER)
        if not monitored_folder.exists():
            monitored_folder.mkdir(parents=True, exist_ok=True)

        # Crear subcarpeta 'processed' para los originales
        processed_folder = monitored_folder / 'processed'
        processed_folder.mkdir(exist_ok=True)

        try:
            # Crear carpeta 'pending' en Main
            pending_folder = Path(settings.MAIN_FOLDER) / 'pending'
            pending_folder.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            logger.error(f"Error al crear la carpeta 'pending': {e}")
            raise

        # Generar nombre único basado en timestamp y nombre original
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        original_name = document.file.name.split('/')[-1]  # Solo el nombre del archivo
        new_name = f"{timestamp}_{original_name}"

        # Mover archivo original a 'processed'
        source_path = document.file.path
        processed_path = processed_folder / original_name
        shutil.move(source_path, processed_path)

        # Crear copia en 'pending'
        pending_path = pending_folder / new_name
        shutil.copy2(processed_path, pending_path)

        # Actualizar campos del documento
        document.original_filename = original_name
        document.imported_from_folder = False  # False porque fue subido manualmente
        document.save(update_fields=['original_filename', 'imported_from_folder'])

@login_required
def get_document_data(request, pk):
    """Obtener datos del documento en formato JSON"""
    user = request.user
    document = get_object_or_404(Document, pk=pk)
    
    # Verificar permisos
    if not user.can_view_all_documents():
        if not (document.assigned_users.filter(id=user.id).exists() or document.created_by == user):
            return JsonResponse({'error': 'Sin permisos'}, status=403)
    
    data = {
        'id': document.id,
        'title': document.title,
        'status': document.status,
        'status_display': document.get_status_display(),
        'payment_status': document.payment_status,
        'payment_status_display': document.get_payment_status_display(),
        'category_id': document.category.id if document.category else None,
        'category_name': document.category.name if document.category else None,
        'document_type_id': document.document_type.id if document.document_type else None,
        'document_type_name': document.document_type.name if document.document_type else None,
        'entity_id': document.entity.id if document.entity else None,
        'entity_name': document.entity.name if document.entity else None,
        'document_date': document.document_date.isoformat() if document.document_date else None,
        'notes': document.notes or '',
        'structured_name': document.get_structured_name(),
        'created_at': document.created_at.isoformat(),
        'file_size': document.file_size
    }
    
    return JsonResponse(data)

@login_required
def serve_document(request, pk):
    """Servir archivo PDF con verificación de permisos"""
    user = request.user
    document = get_object_or_404(Document, pk=pk)
    
    # Verificar permisos
    if not user.can_view_all_documents():
        if not (document.assigned_users.filter(id=user.id).exists() or document.created_by == user):
            raise Http404("Documento no encontrado")
    
    try:
        with open(document.file.path, 'rb') as pdf_file:
            pdf_content = pdf_file.read()
            
            # Crear respuesta con headers optimizados para iframe
            response = HttpResponse(pdf_content, content_type='application/pdf')
            
            # Headers para permitir visualización en iframe
            response['Content-Disposition'] = 'inline; filename="{}"'.format(document.filename)
            response['X-Frame-Options'] = 'SAMEORIGIN'
            response['Content-Length'] = len(pdf_content)
            response['Cache-Control'] = 'public, max-age=3600'
            
            # Headers adicionales para compatibility
            response['Accept-Ranges'] = 'bytes'
            response['Content-Security-Policy'] = "default-src 'self'"
            
            return response
    except FileNotFoundError:
        raise Http404("Archivo no encontrado")
