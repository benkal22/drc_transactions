# DRC_TRANSACTIONS/views.py

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .services import get_currency_conversion
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required

from django.urls import reverse
from allauth.account.signals import user_signed_up, user_logged_in
from django.dispatch import receiver
from transactions.models import Producer
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
        
@login_required
def currency_conversion_template(request):
    return render(request, 'currency_conversion.html')

@login_required
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect('transactions:dashboard')
    else:
        return redirect('transactions:producer_update')


def redirect_view(request):
    user = request.user
    if user.last_login is None or user.last_login == user.date_joined:        
        return redirect('transactions:producers_list')
    else:
        return redirect('transactions:dashboard')

@receiver(user_signed_up)
def user_signed_up_redirect(request, user, **kwargs):
    # Rediriger les nouveaux inscrits vers une URL spécifique
    return redirect('transactions:producers_list')

@receiver(user_logged_in)
def user_logged_in_redirect(request, user, **kwargs):
    if user.last_login is None or user.last_login == user.date_joined:
        # Rediriger les nouveaux inscrits ou les utilisateurs connectés pour la première fois
        return redirect('transactions:producers_list')

    else:
        # Rediriger les anciens utilisateurs
        return redirect('transactions:dashboard')
