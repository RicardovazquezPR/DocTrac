"""
URL configuration for doctrac project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import RedirectView

from documents import admin_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('documents/', include('documents.urls')),
    # path('documents/admin/', admin_views.document_admin, name='document_admin'),
    # Rutas de administración del sistema
    path('admin-dashboard/', admin_views.administration_dashboard, name='administration_dashboard'),
    path('admin-dashboard/entities/', admin_views.manage_persons, name='admin_manage_entities'),
    path('admin-dashboard/entity/create/', admin_views.create_person, name='admin_create_entity'),
    path('admin-dashboard/entity/<int:person_id>/edit/', admin_views.edit_person, name='admin_edit_entity'),
    path('admin-dashboard/categories/', admin_views.manage_categories, name='admin_manage_categories'),
    path('admin-dashboard/category/create/', admin_views.create_category, name='admin_create_category'),
    path('admin-dashboard/category/<int:category_id>/edit/', admin_views.edit_category, name='admin_edit_category'),
    path('admin-dashboard/document-types/', admin_views.manage_document_types, name='admin_manage_document_types'),
    path('admin-dashboard/document-type/create/', admin_views.create_document_type, name='admin_create_document_type'),
    path('admin-dashboard/document-type/<int:doc_type_id>/edit/', admin_views.edit_document_type, name='admin_edit_document_type'),
    path('admin-dashboard/document-type/<int:doc_type_id>/delete/', admin_views.delete_document_type, name='admin_delete_document_type'),
    path('admin-dashboard/rebuild-folders/', admin_views.rebuild_folders, name='admin_rebuild_folders'),
    path('', RedirectView.as_view(url='/documents/', permanent=True)),
]

# Servir archivos media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
