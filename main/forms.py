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

            'name': forms.TextInput(attrs={'class': 'form-control', "id" : "name", 'placeholder': 'Your name'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', "id" : "email",'placeholder': 'Your email'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', "id" : "phone", 'placeholder': 'Your phone'}),
            "comment": forms.Textarea(attrs={'class': 'form-control', "id" : "comment",'placeholder': 'Your message'}),
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
                'required': 'This field is mandatory.',
            },
            'phone': {
                'required': 'This field is mandatory.',
            },
            'email': {
                'required': 'This field is mandatory.',
            },
            
        }