# DRC_TRANSACTIONS/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_currency_conversion
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

class CurrencyConversionView(APIView):
    def get(self, request, *args, **kwargs):
        from_currency = request.query_params.get('from', None)
        to_currency = request.query_params.get('to', None)
        amount = request.query_params.get('amount', None)
        
        if not from_currency or not to_currency or not amount:
            return Response(
                {"error": "Please provide 'from', 'to' and 'amount' query parameters"},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            conversion_data = get_currency_conversion(from_currency, to_currency, amount)
            return Response(conversion_data, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def currency_conversion_template(request):
    return render(request, 'currency_conversion.html')

def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('transactions:dashboard')
    else:
        return redirect('/accounts/login/')

