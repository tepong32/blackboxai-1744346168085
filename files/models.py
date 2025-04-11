from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
import os
import magic

def validate_file_size(value):
    filesize = value.size
    if filesize > 524288000:  # 500MB limit
        raise ValidationError("The maximum file size that can be uploaded is 500MB")

def validate_file_type(value):
    valid_mimetypes = [
        'application/pdf',
        'application/msword',
        'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
        'application/vnd.ms-excel',
        'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
        'image/jpeg',
        'image/png',
        'image/gif',
        'text/plain',
        'application/zip',
        'application/x-rar-compressed'
    ]
    
    file_mime = magic.from_buffer(value.read(1024), mime=True)
    if file_mime not in valid_mimetypes:
        raise ValidationError('Unsupported file type.')
    value.seek(0)

class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('name', 'owner', 'parent')

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(
        upload_to='user_files/%Y/%m/%d/',
        validators=[validate_file_size, validate_file_type]
    )
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    size = models.BigIntegerField(editable=False)
    mime_type = models.CharField(max_length=255, editable=False)

    def save(self, *args, **kwargs):
        if not self.id:  # Only on creation
            self.size = self.file.size
            self.mime_type = magic.from_buffer(self.file.read(1024), mime=True)
            self.file.seek(0)
            
            # Update user's storage usage
            self.owner.used_storage += self.size
            if self.owner.used_storage > self.owner.storage_quota:
                raise ValidationError("Storage quota exceeded")
            self.owner.save()

        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Update user's storage usage
        self.owner.used_storage -= self.size
        self.owner.save()
        super().delete(*args, **kwargs)

    def __str__(self):
        return self.name

class SharedFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE)
    shared_with = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shared_at = models.DateTimeField(auto_now_add=True)
    can_edit = models.BooleanField(default=False)

    class Meta:
        unique_together = ('file', 'shared_with')

    def __str__(self):
        return f"{self.file.name} shared with {self.shared_with.username}"
