from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('folder/<int:folder_id>/', views.folder_view, name='folder_view'),
    path('upload/', views.upload_file, name='upload_file'),
    path('download/<int:file_id>/', views.download_file, name='download_file'),
    path('share/<int:file_id>/', views.share_file, name='share_file'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('delete-file/<int:file_id>/', views.delete_file, name='delete_file'),
    path('delete-folder/<int:folder_id>/', views.delete_folder, name='delete_folder'),
]
