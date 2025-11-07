from rest_framework import serializers
from .models import Book

class BookSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Book
        fields = '__all__'

    def validate_cost_usd(self, value):
        if value <= 0:
            raise serializers.ValidationError('El costo en USD debe ser mayor a 0.')
        return value

    def validate_stock_quantity(self, value):
        if value < 0:
            raise serializers.ValidationError('La cantidad en stock no puede ser negativa.')
        return value

    def validate_isbn(self, value):
        isbn_clean = value.replace('-', '')
        if not (len(isbn_clean) == 10 or len(isbn_clean) == 13) or not isbn_clean.isdigit():
            raise serializers.ValidationError('El ISBN debe tener 10 o 13 dígitos numéricos.')
        return value