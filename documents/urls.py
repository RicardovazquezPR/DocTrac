from django.urls import path
from . import views
from . import admin_views

app_name = 'documents'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('list/', views.DocumentListView.as_view(), name='document_list'),
    path('create/', views.DocumentCreateView.as_view(), name='document_create'),
    path('<int:pk>/', views.document_detail, name='document_detail'),
    path('<int:pk>/data/', views.get_document_data, name='document_data'),
    path('<int:pk>/update/', views.update_document, name='update_document'),
    path('<int:pk>/serve/', views.serve_document, name='serve_document'),
    path('api/document-types/', views.get_document_types_by_category, name='document_types_by_category'),
    
    # URLs de administración
    path('admin/', admin_views.administration_dashboard, name='administration_dashboard'),
    path('admin/entities/', admin_views.manage_persons, name='admin_manage_entities'),
    path('admin/entity/create/', admin_views.create_person, name='admin_create_entity'),
    path('admin/entity/<int:person_id>/edit/', admin_views.edit_person, name='admin_edit_entity'),
    path('admin/categories/', admin_views.manage_categories, name='admin_manage_categories'),
    path('admin/category/create/', admin_views.create_category, name='admin_create_category'),
    path('admin/category/<int:category_id>/edit/', admin_views.edit_category, name='admin_edit_category'),
    path('admin/document-types/', admin_views.manage_document_types, name='admin_manage_document_types'),
    path('admin/document-type/create/', admin_views.create_document_type, name='admin_create_document_type'),
    path('admin/document-type/<int:doc_type_id>/edit/', admin_views.edit_document_type, name='admin_edit_document_type'),
    path('admin/document-type/<int:doc_type_id>/delete/', admin_views.delete_document_type, name='admin_delete_document_type'),
    path('admin/rebuild-folders/', admin_views.rebuild_folders, name='admin_rebuild_folders'),
    path('admin/sync-workfolder/', admin_views.sync_workfolder, name='admin_sync_workfolder'),
]