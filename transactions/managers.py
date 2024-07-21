# transactions/managers.py
from django.contrib.auth.base_user import BaseUserManager
from django.db import models  

class CustomUserManager(BaseUserManager):
    
    def create_user(self, username, email, password=None, **extra_fields):
        """
        Crée et enregistre un utilisateur avec le nom d'utilisateur (username), l'email et le mot de passe donnés.
        """
        if not username:
            raise ValueError('Le nom d\'utilisateur est obligatoire.')
        if not email:
            raise ValueError('L\'email est obligatoire.')

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        """
        Crée et enregistre un superutilisateur avec le nom d'utilisateur (username), l'email et le mot de passe donnés.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(username, email, password, **extra_fields)


class TransactionQuerySet(models.QuerySet):
    def get_sales(self):
        return self.filter(type='sale')
    
    def get_purchases(self):
        return self.filter(type='purchase')
    
    def get_total_purchases(self):
        return self.filter(type='purchase').aggregate(total=models.Sum('total_price_cdf'))['total'] or 0

    def get_total_sales(self):
        return self.filter(type='sale').aggregate(total=models.Sum('total_price_cdf'))['total'] or 0

class TransactionManager(models.Manager):
    def get_queryset(self):
        return TransactionQuerySet(self.model, using=self._db)