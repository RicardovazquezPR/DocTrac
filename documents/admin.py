from django.contrib import admin
from .models import Category, Entity, DocumentType, Document, DocumentHistory

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name', 'value', 'description')
    ordering = ('name',)

@admin.register(Entity)
class EntityAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'is_company', 'is_department')
    list_filter = ('is_company', 'is_department', 'created_at')
    search_fields = ('name', 'value', 'description')
    ordering = ('name',)

@admin.register(DocumentType)
class DocumentTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'value', 'category', 'is_active')
    list_filter = ('category', 'is_active')
    search_fields = ('name', 'value', 'description')
    ordering = ('category', 'name')

class DocumentHistoryInline(admin.TabularInline):
    model = DocumentHistory
    extra = 0
    readonly_fields = ('created_at',)
    fields = ('previous_status', 'new_status', 'changed_by', 'change_reason', 'created_at')

@admin.register(Document)
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'document_type', 'entity', 'status', 'payment_status', 'created_at')
    list_filter = ('status', 'category', 'document_type', 'payment_status', 'created_at')
    search_fields = ('title', 'entity__name', 'notes')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at', 'file_size')
    filter_horizontal = ('assigned_users',)
    inlines = [DocumentHistoryInline]
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('title', 'file')
        }),
        ('Categorización', {
            'fields': ('category', 'document_type', 'entity')
        }),
        ('Fechas', {
            'fields': ('document_date', 'due_date')
        }),
        ('Estado', {
            'fields': ('status', 'payment_status')
        }),
        ('Asignación', {
            'fields': ('assigned_users', 'created_by')
        }),
        ('Información Adicional', {
            'fields': ('notes', 'tags')
        }),
        ('Metadatos', {
            'fields': ('created_at', 'updated_at', 'file_size'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un nuevo objeto
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

@admin.register(DocumentHistory)
class DocumentHistoryAdmin(admin.ModelAdmin):
    list_display = ('document', 'previous_status', 'new_status', 'changed_by', 'created_at')
    list_filter = ('new_status', 'previous_status', 'created_at')
    search_fields = ('document__title',)
    ordering = ('-created_at',)
    readonly_fields = ('created_at',)
