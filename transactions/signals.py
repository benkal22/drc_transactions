# transactions/signals.py
from django.dispatch import receiver
from allauth.account.signals import user_signed_up, user_logged_in
from django.shortcuts import redirect, reverse
from transactions.models import Producer

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
