from django.db import models
from django.core.exceptions import ValidationError

class Book(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    isbn = models.CharField(
        max_length=13,
        unique=True,
        error_messages={
            'unique': 'Ya existe un libro con este ISBN.'
        }
    )
    cost_usd = models.DecimalField(max_digits=10, decimal_places=2)
    selling_price_local = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    stock_quantity = models.IntegerField()
    category = models.CharField(max_length=100)
    supplier_country = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    def clean(self):
        if self.cost_usd <= 0:
            raise ValidationError({'cost_usd': 'El costo en USD debe ser mayor a 0.'})
        if self.stock_quantity < 0:
            raise ValidationError({'stock_quantity': 'La cantidad en stock no puede ser negativa.'})
        isbn_clean = self.isbn.replace('-', '')
        if not (len(isbn_clean) == 10 or len(isbn_clean) == 13) or not isbn_clean.isdigit():
            raise ValidationError({'isbn': 'El ISBN debe tener 10 o 13 dígitos numéricos.'})