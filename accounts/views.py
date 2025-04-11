from django.contrib.auth import login
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, BulkUserUploadForm
from .models import CustomUser
import pandas as pd
from django.core.exceptions import ValidationError
import string
import random

def generate_password(length=12):
    """Generate a random password"""
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(characters) for _ in range(length))

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'
    redirect_authenticated_user = True

@user_passes_test(lambda u: u.is_superuser)
def bulk_user_create(request):
    if request.method == 'POST':
        form = BulkUserUploadForm(request.POST, request.FILES)
        if form.is_valid():
            file = request.FILES['file']
            
            try:
                # Read the file
                if file.name.endswith('.csv'):
                    df = pd.read_csv(file)
                else:
                    df = pd.read_excel(file)

                # Process each row
                created_users = []
                errors = []
                
                for index, row in df.iterrows():
                    try:
                        # Generate password
                        password = generate_password()
                        
                        # Create user
                        user = CustomUser(
                            first_name=row['first_name'],
                            last_name=row['last_name'],
                            middle_initial=row.get('middle_initial', ''),
                            email=row['email'],
                        )
                        
                        # Username will be automatically generated on save
                        user.save()
                        
                        # Set password
                        user.set_password(password)
                        user.save()
                        
                        created_users.append({
                            'username': user.username,
                            'email': user.email,
                            'password': password
                        })
                        
                    except Exception as e:
                        errors.append(f"Error in row {index + 2}: {str(e)}")

                if errors:
                    messages.warning(request, 
                        "Some users could not be created:\n" + "\n".join(errors))
                
                if created_users:
                    # Render template with created users and their credentials
                    return render(request, 'registration/bulk_create_results.html', {
                        'created_users': created_users
                    })
                    
            except Exception as e:
                messages.error(request, f"Error processing file: {str(e)}")
                return redirect('bulk_user_create')
    else:
        form = BulkUserUploadForm()
    
    return render(request, 'registration/bulk_create.html', {'form': form})

@login_required
def profile(request):
    storage_used_mb = round(request.user.used_storage / (1024 * 1024), 2)
    storage_quota_mb = round(request.user.storage_quota / (1024 * 1024), 2)
    storage_percentage = (storage_used_mb / storage_quota_mb) * 100 if storage_quota_mb > 0 else 0
    
    context = {
        'storage_used': storage_used_mb,
        'storage_quota': storage_quota_mb,
        'storage_percentage': storage_percentage,
    }
    return render(request, 'registration/profile.html', context)
