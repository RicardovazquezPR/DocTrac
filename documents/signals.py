from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Document, DocumentHistory

User = get_user_model()

@receiver(pre_save, sender=Document)
def track_document_changes(sender, instance, **kwargs):
    """Trackear cambios de estado en documentos"""
    if instance.pk:  # Solo si el documento ya existe
        try:
            old_document = Document.objects.get(pk=instance.pk)
            instance._old_status = old_document.status
        except Document.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Document)
def create_document_history(sender, instance, created, **kwargs):
    """Crear entrada en historial cuando cambie el estado"""
    if created:
        # Documento nuevo
        DocumentHistory.objects.create(
            document=instance,
            previous_status=None,
            new_status=instance.status,
            changed_by=instance.created_by,
            change_reason='Documento creado'
        )
    else:
        # Documento actualizado
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            DocumentHistory.objects.create(
                document=instance,
                previous_status=old_status,
                new_status=instance.status,
                changed_by=getattr(instance, '_changed_by', None),
                change_reason=getattr(instance, '_change_reason', 'Estado actualizado')
            )