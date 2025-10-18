from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Usuario extendido con niveles de acceso"""
    
    USER_ROLES = [
        ('admin', 'Administrador'),
        ('manager', 'Gerente'),
        ('user', 'Usuario'),
    ]
    
    role = models.CharField(
        max_length=20, 
        choices=USER_ROLES, 
        default='user',
        verbose_name='Rol'
    )
    phone = models.CharField(
        max_length=15, 
        blank=True, 
        null=True,
        verbose_name='Teléfono'
    )
    department = models.CharField(
        max_length=100, 
        blank=True, 
        null=True,
        verbose_name='Departamento'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de creación'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='Fecha de actualización'
    )
    
    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
    
    def __str__(self):
        return f"{self.username} - {self.get_role_display()}"
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_manager(self):
        return self.role in ['admin', 'manager']
    
    def can_view_all_documents(self):
        return self.role == 'admin'
