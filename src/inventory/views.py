from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from .models import Book
from .serializers import BookSerializer
import requests
from django.utils import timezone

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    @action(detail=False, methods=['get'], url_path='search')
    def search_by_category(self, request):
        category = request.query_params.get('category')
        if not category:
            return Response({'error': 'Debe proporcionar el parámetro category.'}, status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(category__icontains=category)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'], url_path='low-stock')
    def low_stock(self, request):
        threshold = request.query_params.get('threshold', 10)
        try:
            threshold = int(threshold)
        except ValueError:
            return Response({'error': 'El parámetro threshold debe ser un número entero.'}, status=status.HTTP_400_BAD_REQUEST)
        books = Book.objects.filter(stock_quantity__lt=threshold)
        serializer = self.get_serializer(books, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['post'], url_path='calculate-price')
    def calculate_price(self, request, pk=None):
        
        book = self.get_object()
        country_currency_map = {
            'ES': 'EUR', 'US': 'USD', 'GB': 'GBP', 'MX': 'MXN', 'AR': 'ARS', 'BR': 'BRL', 'CL': 'CLP', 'CO': 'COP', 'PE': 'PEN', 'UY': 'UYU', 'PY': 'PYG', 'EC': 'USD', 'FR': 'EUR', 'DE': 'EUR', 'IT': 'EUR', 'PT': 'EUR', 'JP': 'JPY', 'CN': 'CNY', 'IN': 'INR', 'CA': 'CAD', 'AU': 'AUD', 'CH': 'CHF', 'RU': 'RUB', 'KR': 'KRW', 'ZA': 'ZAR', 'VE': 'VES', 'CR': 'CRC', 'DO': 'DOP', 'GT': 'GTQ', 'HN': 'HNL', 'NI': 'NIO', 'SV': 'USD', 'PA': 'USD', 'PR': 'USD', 'CU': 'CUP', 'BO': 'BOB', 'BR': 'BRL', 'EC': 'USD', 'PY': 'PYG', 'PE': 'PEN', 'UY': 'UYU', 'CL': 'CLP', 'CO': 'COP', 'AR': 'ARS', 'MX': 'MXN', 'ES': 'EUR', 'PT': 'EUR', 'FR': 'EUR', 'IT': 'EUR', 'DE': 'EUR', 'GB': 'GBP', 'JP': 'JPY', 'CN': 'CNY', 'IN': 'INR', 'KR': 'KRW', 'RU': 'RUB', 'CA': 'CAD', 'AU': 'AUD', 'CH': 'CHF', 'ZA': 'ZAR', 'VE': 'VES', 'CR': 'CRC', 'DO': 'DOP', 'GT': 'GTQ', 'HN': 'HNL', 'NI': 'NIO', 'SV': 'USD', 'PA': 'USD', 'PR': 'USD', 'CU': 'CUP', 'BO': 'BOB'
        }
        currency = country_currency_map.get(book.supplier_country.upper(), 'USD')

        try:
            response = requests.get('https://api.exchangerate-api.com/v4/latest/USD', timeout=5)
            data = response.json()
            exchange_rate = data['rates'].get(currency, 1)
        except Exception:
            exchange_rate = 1
        cost_local = float(book.cost_usd) * float(exchange_rate)
        margin_percentage = 40
        selling_price_local = round(cost_local * (1 + margin_percentage / 100), 2)
        book.selling_price_local = selling_price_local
        book.save()
        result = {
            'book_id': book.id,
            'cost_usd': float(book.cost_usd),
            'exchange_rate': exchange_rate,
            'cost_local': round(cost_local, 2),
            'margin_percentage': margin_percentage,
            'selling_price_local': selling_price_local,
            'currency': currency,
            'calculation_timestamp': timezone.now().isoformat()
        }
        return Response(result)