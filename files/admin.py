from django.contrib import admin
from .models import File, Folder, SharedFile

@admin.register(Folder)
class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'parent', 'created_at', 'updated_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'owner__username', 'owner__email')
    raw_id_fields = ('owner', 'parent')
    date_hierarchy = 'created_at'

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'folder', 'size_display', 'mime_type', 'uploaded_at')
    list_filter = ('owner', 'mime_type', 'uploaded_at')
    search_fields = ('name', 'owner__username', 'owner__email')
    raw_id_fields = ('owner', 'folder')
    date_hierarchy = 'uploaded_at'
    readonly_fields = ('size', 'mime_type')

    def size_display(self, obj):
        """Display file size in human-readable format"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if obj.size < 1024:
                return f"{obj.size:.2f} {unit}"
            obj.size /= 1024
        return f"{obj.size:.2f} TB"
    size_display.short_description = 'Size'

@admin.register(SharedFile)
class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'shared_with', 'shared_at', 'can_edit')
    list_filter = ('can_edit', 'shared_at')
    search_fields = ('file__name', 'shared_with__username', 'shared_with__email')
    raw_id_fields = ('file', 'shared_with')
    date_hierarchy = 'shared_at'
