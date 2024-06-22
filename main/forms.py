from django import forms
from main.models import Contact

class ContactForm(forms.ModelForm):
    def clean_name(self):
            name = self.cleaned_data['name']
            return f'{name.upper()}'

    class Meta:
        
        model = Contact
        fields = ('name', 'email', 'phone', 'comment')

        widgets = {

            'name': forms.TextInput(attrs={'class': 'form-control', "id" : "name", 'placeholder': 'Your Name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', "id" : "email",'placeholder': 'Your Email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', "id" : "phone", 'placeholder': 'Your Phone'}),
            "comment": forms.Textarea(attrs={'class': 'form-control', "id" : "comment",'placeholder': 'Your Message'}),
        }

        labels = {
            'name': 'Name',
            'email': 'Email',
            'phone': 'Phone',
            'comment': 'Comment',
        }

        help_texts = {
            'phone': 'Enter the phone number in the format : +380XXXXXXXXX',
        }

        error_messages = {
            'name': {
                'required': 'This field is required.',
            },
            'phone': {
                'required': 'This field is required.',
            },
            'email': {
                'required': 'This field is required.',
            },
            
        }