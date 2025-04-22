from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.core.exceptions import PermissionDenied
from django.contrib import messages
from django.db.models import Q
from .models import File, Folder, SharedFile
from django.conf import settings
import os
import mimetypes

@login_required
def dashboard(request):
    """Display user's files and folders"""
    folders = Folder.objects.filter(
        Q(owner=request.user) | 
        Q(file__sharedfile__shared_with=request.user)
    ).distinct()
    
    # Only show files that are not in any folder
    files = File.objects.filter(
        (Q(owner=request.user) | Q(sharedfile__shared_with=request.user)) &
        Q(folder__isnull=True)
    ).distinct()
    
    context = {
        'folders': folders,
        'files': files,
    }
    return render(request, 'filemanager/dashboard.html', context)

@login_required
def folder_view(request, folder_id):
    """Display contents of a specific folder"""
    folder = get_object_or_404(Folder, id=folder_id)
    
    # Check if user has access to this folder
    if folder.owner != request.user and not SharedFile.objects.filter(
        file__folder=folder, shared_with=request.user).exists():
        raise PermissionDenied
    
    files = File.objects.filter(folder=folder)
    subfolders = Folder.objects.filter(parent=folder)
    
    context = {
        'folder': folder,
        'files': files,
        'subfolders': subfolders,
    }
    return render(request, 'filemanager/folder.html', context)

@login_required
def upload_file(request):
    """Handle file upload"""
    if request.method == 'POST':
        folder_id = request.POST.get('folder')
        folder = None if not folder_id else get_object_or_404(Folder, id=folder_id)
        
        if folder and folder.owner != request.user:
            raise PermissionDenied
        
        files = request.FILES.getlist('files')
        
        for uploaded_file in files:
            try:
                file = File(
                    name=uploaded_file.name,
                    file=uploaded_file,
                    owner=request.user,
                    folder=folder
                )
                file.save()
                messages.success(request, f'Successfully uploaded {file.name}')
            except Exception as e:
                messages.error(request, f'Error uploading {uploaded_file.name}: {str(e)}')
        
        if folder:
            return redirect('folder_view', folder_id=folder.id)
        return redirect('dashboard')
    
    folders = Folder.objects.filter(owner=request.user)
    return render(request, 'filemanager/upload.html', {'folders': folders})

@login_required
def download_file(request, file_id):
    """Handle file download"""
    file = get_object_or_404(File, id=file_id)
    
    # Check if user has access to this file
    if file.owner != request.user and not SharedFile.objects.filter(
        file=file, shared_with=request.user).exists():
        raise PermissionDenied
    
    file_path = file.file.path
    if os.path.exists(file_path):
        with open(file_path, 'rb') as fh:
            response = HttpResponse(fh.read(), content_type=mimetypes.guess_type(file_path)[0])
            response['Content-Disposition'] = f'attachment; filename={file.name}'
            return response
    raise Http404

@login_required
def share_file(request, file_id):
    """Share file with other users"""
    file = get_object_or_404(File, id=file_id)
    
    if file.owner != request.user:
        raise PermissionDenied
    
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        can_edit = request.POST.get('can_edit') == 'true'
        
        try:
            shared_with = CustomUser.objects.get(id=user_id)
            SharedFile.objects.create(
                file=file,
                shared_with=shared_with,
                can_edit=can_edit
            )
            messages.success(request, f'File shared with {shared_with.get_full_name()}')
        except Exception as e:
            messages.error(request, f'Error sharing file: {str(e)}')
        
        return redirect('dashboard')
    
    # Get users to share with (excluding file owner and users already shared with)
    users = CustomUser.objects.exclude(
        Q(id=request.user.id) |
        Q(sharedfile__file=file)
    )
    
    return render(request, 'filemanager/share.html', {
        'file': file,
        'users': users
    })

@login_required
def create_folder(request):
    """Create a new folder"""
    if request.method == 'POST':
        name = request.POST.get('name')
        parent_id = request.POST.get('parent')
        
        try:
            parent = None if not parent_id else get_object_or_404(Folder, id=parent_id)
            
            if parent and parent.owner != request.user:
                raise PermissionDenied
            
            folder = Folder.objects.create(
                name=name,
                owner=request.user,
                parent=parent
            )
            messages.success(request, f'Folder "{name}" created successfully')
            
            return redirect('dashboard' if not parent else 'folder_view', folder_id=parent.id)
        except Exception as e:
            messages.error(request, f'Error creating folder: {str(e)}')
            return redirect('dashboard')
    
    parent_id = request.GET.get('parent')
    parent = None if not parent_id else get_object_or_404(Folder, id=parent_id)
    
    return render(request, 'filemanager/create_folder.html', {'parent': parent})

@login_required
def delete_file(request, file_id):
    """Delete a file"""
    file = get_object_or_404(File, id=file_id)
    
    if file.owner != request.user:
        raise PermissionDenied
    
    try:
        file.delete()
        messages.success(request, f'File "{file.name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting file: {str(e)}')
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))

@login_required
def delete_folder(request, folder_id):
    """Delete a folder"""
    folder = get_object_or_404(Folder, id=folder_id)
    
    if folder.owner != request.user:
        raise PermissionDenied
    
    try:
        folder.delete()
        messages.success(request, f'Folder "{folder.name}" deleted successfully')
    except Exception as e:
        messages.error(request, f'Error deleting folder: {str(e)}')
    
    return redirect(request.META.get('HTTP_REFERER', 'dashboard'))
