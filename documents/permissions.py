from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from .models import Document

class DocumentPermissionMixin(UserPassesTestMixin):
    """Mixin para verificar permisos de documentos"""
    
    def test_func(self):
        user = self.request.user
        if not user.is_authenticated:
            return False
        
        # Admin puede ver todo
        if user.can_view_all_documents():
            return True
        
        # Obtener el documento
        document = self.get_object()
        
        # Verificar si el usuario tiene acceso al documento
        return (document.assigned_users.filter(id=user.id).exists() or 
                document.created_by == user)

def user_can_access_document(user, document):
    """Verificar si un usuario puede acceder a un documento"""
    if user.can_view_all_documents():
        return True
    
    return (document.assigned_users.filter(id=user.id).exists() or 
            document.created_by == user)

def get_user_documents(user):
    """Obtener documentos accesibles para un usuario"""
    if user.can_view_all_documents():
        return Document.objects.all()
    else:
        return Document.objects.filter(
            Q(assigned_users=user) | Q(created_by=user)
        ).distinct()

class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere permisos de administrador"""
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_admin()

class ManagerRequiredMixin(UserPassesTestMixin):
    """Mixin que requiere permisos de manager o admin"""
    
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.is_manager()