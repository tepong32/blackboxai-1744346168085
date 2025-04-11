from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import pandas as pd
from django.core.exceptions import ValidationError

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'middle_initial')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'middle_initial')

class BulkUserUploadForm(forms.Form):
    file = forms.FileField(
        help_text='Upload CSV/Excel file with columns: first_name, last_name, middle_initial, email'
    )

    def clean_file(self):
        file = self.cleaned_data['file']
        if not file.name.endswith(('.csv', '.xlsx', '.xls')):
            raise ValidationError('Please upload a CSV or Excel file.')

        try:
            if file.name.endswith('.csv'):
                df = pd.read_csv(file)
            else:
                df = pd.read_excel(file)

            required_columns = ['first_name', 'last_name', 'email']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                raise ValidationError(f'Missing required columns: {", ".join(missing_columns)}')

            # Validate email format
            invalid_emails = []
            for idx, email in enumerate(df['email']):
                if not isinstance(email, str) or '@' not in email:
                    invalid_emails.append(f"Row {idx + 2}: {email}")

            if invalid_emails:
                raise ValidationError(f'Invalid email formats found:\n{chr(10).join(invalid_emails)}')

            return file
        except Exception as e:
            raise ValidationError(f'Error processing file: {str(e)}')
