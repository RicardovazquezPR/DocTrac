from celery import shared_task
import shutil
from pathlib import Path

def move_to_processed(source_path, processed_path):
    shutil.move(source_path, processed_path)

def copy_to_pending(processed_path, pending_path):
    shutil.copy2(processed_path, pending_path)

@shared_task
def process_document(source_path, processed_path, pending_path):
    move_to_processed(source_path, processed_path)
    copy_to_pending(processed_path, pending_path)