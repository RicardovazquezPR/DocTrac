from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import FileExtensionValidator
import os

User = get_user_model()

class Category(models.Model):
    """Categorías de documentos"""
    name = models.CharField(
        max_length=100, 
        verbose_name='Nombre',
        help_text='Nombre que se muestra en los dropdowns'
    )
    value = models.CharField(
        max_length=50,
        verbose_name='Valor',
        help_text='Valor usado en nombres de archivos PDF (sin espacios ni caracteres especiales)',
        unique=True,
        default='default_category'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada de la categoría'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    applies_to_all = models.BooleanField(
        default=True,
        verbose_name='Aplica a todas las entidades',
        help_text='Si está marcado, esta categoría se aplicará a todas las entidades'
    )
    applicable_entities = models.ManyToManyField(
        'Entity',
        blank=True,
        related_name='applicable_categories',
        verbose_name='Entidades aplicables',
        help_text='Selecciona las entidades a las que aplica esta categoría (solo si no aplica a todas)'
    )
    
    class Meta:
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        """Override save para crear carpetas automáticamente"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new:
            self.create_category_folders()
    
    def create_category_folders(self):
        """Crea carpetas de esta categoría en las entidades aplicables"""
        import os
        
        # Obtener entidades aplicables
        if self.applies_to_all:
            entities = Entity.objects.filter(auto_create_folder=True)
        else:
            entities = self.applicable_entities.filter(auto_create_folder=True)
        
        # Limpiar nombre de categoría
        cat_clean_name = "".join(c for c in self.name if c.isalnum() or c in (' ', '-', '_')).strip()
        cat_clean_name = cat_clean_name.replace(' ', '_')
        
        for entity in entities:
            if entity.folder_path and os.path.exists(entity.folder_path):
                cat_path = os.path.join(entity.folder_path, cat_clean_name)
                try:
                    os.makedirs(cat_path, exist_ok=True)
                except Exception as e:
                    print(f"Error creando carpeta de categoría {self.name} para {entity.name}: {e}")
    
    def update_entity_folders(self):
        """Actualiza las carpetas cuando cambian las entidades aplicables"""
        self.create_category_folders()

class Entity(models.Model):
    """Entidades, departamentos o compañías asociadas a documentos"""
    name = models.CharField(
        max_length=200,
        verbose_name='Nombre',
        help_text='Nombre que se muestra en los dropdowns'
    )
    value = models.CharField(
        max_length=100,
        verbose_name='Valor',
        help_text='Valor usado en nombres de archivos PDF (sin espacios ni caracteres especiales)',
        unique=True,
        default='default_entity'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada de la entidad'
    )
    is_company = models.BooleanField(
        default=False,
        verbose_name='Es empresa'
    )
    is_department = models.BooleanField(
        default=False,
        verbose_name='Es departamento',
        help_text='Marca si es un departamento interno de la entidad'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    folder_path = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name='Ruta de carpeta',
        help_text='Ruta de la carpeta asociada a esta entidad'
    )
    auto_create_folder = models.BooleanField(
        default=True,
        verbose_name='Crear carpeta automáticamente',
        help_text='Crear carpeta automáticamente en el sistema de archivos'
    )
    
    class Meta:
        verbose_name = 'Entidad/Departamento'
        verbose_name_plural = 'Entidades/Departamentos'
        ordering = ['name']
    
    def __str__(self):
        if self.is_department:
            return f"{self.name} (Departamento)"
        elif self.is_company:
            return f"{self.name} (Empresa)"
        else:
            return f"{self.name} (Entidad)"
    
    @property
    def type_display(self):
        """Retorna el tipo de entidad para mostrar en la interfaz"""
        from django.conf import settings
        
        if hasattr(settings, 'SYSTEM_USAGE_TYPE'):
            if settings.SYSTEM_USAGE_TYPE == 'empresa':
                return 'Departamento' if self.is_department else ('Empresa' if self.is_company else 'Externo')
            else:
                return 'Empresa' if self.is_company else 'Entidad'
        
        return 'Empresa' if self.is_company else 'Entidad'
    
    def save(self, *args, **kwargs):
        """Override save para crear carpeta automáticamente"""
        is_new = self.pk is None
        super().save(*args, **kwargs)
        
        if is_new and self.auto_create_folder:
            self.create_folder_structure()
    
    def create_folder_structure(self):
        """Crea la estructura de carpetas para esta entidad"""
        from django.conf import settings
        import os
        
        if not hasattr(settings, 'MAIN_FOLDER'):
            return
        
        # Limpiar nombre para usar como carpeta
        clean_name = "".join(c for c in self.name if c.isalnum() or c in (' ', '-', '_')).strip()
        clean_name = clean_name.replace(' ', '_')
        
        # Crear ruta base
        base_path = os.path.join(settings.MAIN_FOLDER, clean_name)
        
        try:
            os.makedirs(base_path, exist_ok=True)
            
            # Guardar la ruta
            if not self.folder_path:
                self.folder_path = base_path
                Entity.objects.filter(pk=self.pk).update(folder_path=base_path)
            
            # Crear subcarpetas para categorías existentes que apliquen
            from .models import Category
            categories = Category.objects.filter(is_active=True)
            
            for category in categories:
                # Verificar si esta categoría aplica a esta entidad
                if hasattr(category, 'applies_to_all') and category.applies_to_all:
                    cat_clean_name = "".join(c for c in category.name if c.isalnum() or c in (' ', '-', '_')).strip()
                    cat_clean_name = cat_clean_name.replace(' ', '_')
                    cat_path = os.path.join(base_path, cat_clean_name)
                    os.makedirs(cat_path, exist_ok=True)
                elif hasattr(category, 'applicable_entities') and self in category.applicable_entities.all():
                    cat_clean_name = "".join(c for c in category.name if c.isalnum() or c in (' ', '-', '_')).strip()
                    cat_clean_name = cat_clean_name.replace(' ', '_')
                    cat_path = os.path.join(base_path, cat_clean_name)
                    os.makedirs(cat_path, exist_ok=True)
                    
        except Exception as e:
            print(f"Error creando carpeta para {self.name}: {e}")
    
    def get_folder_path(self):
        """Retorna la ruta de carpeta, creándola si no existe"""
        if not self.folder_path and self.auto_create_folder:
            self.create_folder_structure()
        return self.folder_path or ""

class DocumentType(models.Model):
    """Tipos de documentos"""
    name = models.CharField(
        max_length=100,
        verbose_name='Nombre',
        help_text='Nombre que se muestra en los dropdowns'
    )
    value = models.CharField(
        max_length=50,
        verbose_name='Valor',
        help_text='Valor usado en nombres de archivos PDF (sin espacios ni caracteres especiales)',
        default='default_doc_type'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='document_types',
        verbose_name='Categoría'
    )
    description = models.TextField(
        blank=True, 
        null=True,
        verbose_name='Descripción',
        help_text='Descripción detallada del tipo de documento'
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name='Activo'
    )
    
    class Meta:
        verbose_name = 'Tipo de Documento'
        verbose_name_plural = 'Tipos de Documentos'
        ordering = ['category', 'name']
        unique_together = [['category', 'value']]
    
    def __str__(self):
        return f"{self.category.name} - {self.name}"

def document_file_upload_path(instance, filename):
    """Genera el path para subir documentos PDF"""
    import os
    from datetime import datetime
    
    # Usar fecha actual ya que instance.created_at puede ser None
    now = datetime.now()
    year = now.year
    month = now.month
    
    # Limpiar nombre de archivo
    name, ext = os.path.splitext(filename)
    clean_name = "".join(c for c in name if c.isalnum() or c in (' ', '-', '_')).rstrip()
    clean_filename = f"{clean_name}{ext}"
    
    return f"documents/{year}/{month:02d}/{clean_filename}"

class Document(models.Model):
    """Documento principal"""
    
    STATUS_CHOICES = [
        ('pending', 'Pendiente'),
        ('scanned', 'Escaneado'),
        ('digitized', 'Digitalizado'),
        ('categorized', 'Categorizado'),
        ('approved', 'Aprobado'),
        ('archived', 'Archivado'),
    ]
    
    PAYMENT_STATUS = [
        ('paid', 'Pagado'),
        ('pending', 'Pendiente'),
        ('overdue', 'Vencido'),
        ('not_applicable', 'No Aplica'),
    ]
    
    # Información básica
    title = models.CharField(
        max_length=255,
        verbose_name='Título'
    )
    file = models.FileField(
        upload_to=document_file_upload_path,
        validators=[FileExtensionValidator(allowed_extensions=['pdf'])],
        verbose_name='Archivo PDF'
    )
    
    # Categorización
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='documents',
        verbose_name='Categoría'
    )
    document_type = models.ForeignKey(
        DocumentType,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='documents',
        verbose_name='Tipo de Documento'
    )
    entity = models.ForeignKey(
        Entity,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='Entidad'
    )
    
    # Fechas
    document_date = models.DateField(
        null=True, blank=True,
        verbose_name='Fecha del Documento'
    )
    due_date = models.DateField(
        null=True, blank=True,
        verbose_name='Fecha de Vencimiento'
    )
    
    # Estado y pagos
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending',
        verbose_name='Estado'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='not_applicable',
        verbose_name='Estado de Pago'
    )
    
    # Permisos y asignación
    assigned_users = models.ManyToManyField(
        User,
        blank=True,
        related_name='assigned_documents',
        verbose_name='Usuarios Asignados'
    )
    created_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        related_name='created_documents',
        verbose_name='Creado por'
    )
    
    # Metadatos
    notes = models.TextField(
        blank=True, null=True,
        verbose_name='Notas'
    )
    tags = models.CharField(
        max_length=255, 
        blank=True, null=True,
        help_text='Etiquetas separadas por comas',
        verbose_name='Etiquetas'
    )
    original_filename = models.CharField(
        max_length=255,
        blank=True, null=True,
        verbose_name='Nombre archivo original',
        help_text='Nombre original del archivo antes de procesamiento'
    )
    imported_from_folder = models.BooleanField(
        default=False,
        verbose_name='Importado desde carpeta',
        help_text='Indica si fue importado automáticamente desde la carpeta de monitoreo'
    )
    
    # Fechas de sistema
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'
        ordering = ['-created_at']
        permissions = [
            ('can_view_all_documents', 'Puede ver todos los documentos'),
            ('can_approve_documents', 'Puede aprobar documentos'),
        ]
    
    def __str__(self):
        return self.title
    
    @property
    def filename(self):
        """Retorna solo el nombre del archivo"""
        return os.path.basename(self.file.name) if self.file else ''
    
    @property
    def file_size(self):
        """Retorna el tamaño del archivo en MB"""
        try:
            return round(self.file.size / 1024 / 1024, 2) if self.file else 0
        except:
            return 0
    
    def get_structured_name(self):
        """Genera un nombre estructurado usando códigos cortos: Entidad_Categoría_TipoDocumento_Fecha"""
        parts = []
        
        # 1. Entidad (usando el valor corto)
        if self.entity:
            entity_value = getattr(self.entity, 'value', None) or self.entity.name.replace(' ', '_')
            parts.append(entity_value)
        
        # 2. Categoría (usando el valor corto)
        if self.category:
            category_value = getattr(self.category, 'value', None) or self.category.name.replace(' ', '_')
            parts.append(category_value)
        
        # 3. Tipo de Documento (usando el valor corto)
        if self.document_type:
            doc_type_value = getattr(self.document_type, 'value', None) or self.document_type.name.replace(' ', '_')
            parts.append(doc_type_value)
        
        # 4. Fecha (al final)
        if self.document_date:
            # Manejar tanto objetos datetime como strings
            if hasattr(self.document_date, 'strftime'):
                parts.append(self.document_date.strftime('%Y%m%d'))
            elif isinstance(self.document_date, str):
                # Si es string, intentar parsearlo
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(self.document_date, '%Y-%m-%d')
                    parts.append(parsed_date.strftime('%Y%m%d'))
                except ValueError:
                    # Si no se puede parsear, usar como está
                    parts.append(str(self.document_date).replace('-', ''))
        
        return '_'.join(parts) if parts else self.title
    
    def get_display_name(self):
        """Genera un nombre legible con los nombres completos para mostrar en el UI"""
        parts = []
        
        # 1. Entidad (nombre completo)
        if self.entity:
            parts.append(self.entity.name)
        
        # 2. Categoría (nombre completo)
        if self.category:
            parts.append(self.category.name)
        
        # 3. Tipo de Documento (nombre completo)
        if self.document_type:
            parts.append(self.document_type.name)
        
        # 4. Fecha (formato legible)
        if self.document_date:
            if hasattr(self.document_date, 'strftime'):
                parts.append(self.document_date.strftime('%d/%m/%Y'))
            elif isinstance(self.document_date, str):
                try:
                    from datetime import datetime
                    parsed_date = datetime.strptime(self.document_date, '%Y-%m-%d')
                    parts.append(parsed_date.strftime('%d/%m/%Y'))
                except ValueError:
                    parts.append(str(self.document_date))
        
        return ' - '.join(parts) if parts else self.title

class DocumentHistory(models.Model):
    """Historial de cambios de estado de documentos"""
    document = models.ForeignKey(
        Document,
        on_delete=models.CASCADE,
        related_name='history',
        verbose_name='Documento'
    )
    previous_status = models.CharField(
        max_length=20,
        choices=Document.STATUS_CHOICES,
        null=True, blank=True,
        verbose_name='Estado Anterior'
    )
    new_status = models.CharField(
        max_length=20,
        choices=Document.STATUS_CHOICES,
        verbose_name='Nuevo Estado'
    )
    changed_by = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name='Cambiado por'
    )
    change_reason = models.TextField(
        blank=True, null=True,
        verbose_name='Motivo del cambio'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha del cambio'
    )
    
    class Meta:
        verbose_name = 'Historial de Documento'
        verbose_name_plural = 'Historial de Documentos'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.document.title} - {self.new_status} ({self.created_at})"
