import re
from django import forms


class CreateOrderForm(forms.Form):

    first_name = forms.CharField(
        label= "First name*:"
    )
    last_name = forms.CharField(
        label= "Last name*:"
    )
    phone_number = forms.CharField(
        label= "Phone number*:"
    )
    requires_delivery = forms.ChoiceField(
        label= "Requires delivery:",
        choices=[
            ("0", False),
            ("1", True),
            ],
        )
    delivery_address = forms.CharField(
        required=False,
        label= "Delivery Address*:",
    )
    payment_on_get = forms.ChoiceField(
        label= "Payment on get:",
        choices=[
            ("0", 'False'),
            ("1", 'True'),
            ],
        )

    def clean_phone_number(self):
        data = self.cleaned_data['phone_number']

        if not data.isdigit():
            raise forms.ValidationError("The phone number must contain only numbers")
        
        pattern = re.compile(r"^\+?(380)?\d{9,15}$")  # (r'^\d{10}$')
        if not pattern.match(data):
            raise forms.ValidationError("Invalid number format")

        return data