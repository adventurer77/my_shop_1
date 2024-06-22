from django.db import models
from django.core.validators import RegexValidator

# Create your models here.


class Contact(models.Model):
    phone_regex = RegexValidator(
        regex=r"^\+?(380)?\d{9,15}$",
        message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.",
    )

    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20, validators=[phone_regex])
    comment = models.TextField(blank=True, null=True)

    is_confirmed = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f'{self.name} - Created: {self.date_created} | Updated: {self.date_updated}'

    class Meta:
        db_table = "contact"
        verbose_name = "Contact"
        verbose_name_plural = "Contacts"
        ordering = ["-date_created"]
