from django import forms
from .models import Supplier, Producer, Client, Transaction, Product, UniqueSector, Stock
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone
from django import forms
from .models import Supplier, Product, UniqueSector, Country, Province

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = [
            'company_name', 'manager_name', 'tax_code', 'nrc', 'nat_id',
            'product', 'sector_label', 'photo', 'address', 'email',
            'phone_number', 'country', 'province', 'initial_balance', 'is_approved'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'manager_name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'tax_code': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'nrc': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'nat_id': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'product': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'sector_label': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'country': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'province': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'initial_balance': forms.NumberInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'is_approved': forms.CheckboxInput(attrs={
                'class': 'form-checkbox h-4 w-4 text-purple-600 transition duration-150 ease-in-out'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['product'].initial = self.instance.product.values_list('id', flat=True)
            self.fields['sector_label'].initial = self.instance.sector_label_id
        self.fields['product'].queryset = Product.objects.all()
        self.fields['sector_label'].queryset = UniqueSector.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        products = self.cleaned_data.get('product')
        
        if commit:
            instance.save()
            if products:
                instance.product.set(products)
        return instance

    def clean(self):
        cleaned_data = super().clean()
        country = cleaned_data.get("country")
        province = cleaned_data.get("province")

        if country and country.country == 'Congo (Kinshasa)' and not province:
            self.add_error('province', "Le champ province est requis pour le pays Congo (Kinshasa).")
        
        return cleaned_data

class SupplierForm(forms.ModelForm):
    class Meta:
        model = Supplier
        fields = [
            'category', 'name', 'manager_name', 'tax_code', 'nrc', 'nat_id',
            'product', 'sector_label', 'photo', 'address', 'email',
            'phone_number', 'country', 'province'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'manager_name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'tax_code': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'nrc': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'nat_id': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'product': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'sector_label': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'country': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'province': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['sector_label'].initial = self.instance.sector_label.values_list('id', flat=True)
            self.fields['product'].initial = self.instance.product.values_list('id', flat=True)
        self.fields['product'].queryset = Product.objects.all()
        
    def save(self, commit=True):
        instance = super().save(commit=False)
        sector_labels = self.cleaned_data.get('sector_label')
        products = self.cleaned_data.get('product')
        
        if commit:
            instance.save()
            if sector_labels:
                instance.sector_label.set(sector_labels)
            if products:
                instance.product.set(products)
        return instance

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        name = cleaned_data.get("name")
        country = cleaned_data.get("country")
        province = cleaned_data.get("province")

        if category == 'individual' and Supplier.objects.filter(name=name, category='individual').exclude(pk=self.instance.pk).exists():
            self.add_error('name', f"Un fournisseur individuel avec le nom '{name}' existe déjà.")
        
        if category == 'enterprise' and Supplier.objects.filter(name=name, category='enterprise').exclude(pk=self.instance.pk).exists():
            self.add_error('name', f"Une entreprise fournisseur avec le nom '{name}' existe déjà.")
        
        if country and country.country == 'Congo (Kinshasa)' and not province:
            self.add_error('province', "Le champ province est requis pour le pays Congo (Kinshasa).")
        
        return cleaned_data

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = [
            'category', 'name', 'manager_name', 'tax_code', 'nrc', 'nat_id',
            'product', 'sector_label', 'photo', 'address', 'email',
            'phone_number', 'country', 'province'
        ]
        widgets = {
            'category': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
            }),
            'name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'manager_name': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'tax_code': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'nrc': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'nat_id': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'product': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'sector_label': forms.SelectMultiple(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'photo': forms.ClearableFileInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'address': forms.Textarea(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'phone_number': forms.TextInput(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            }),
            'country': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
            'province': forms.Select(attrs={
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select select2'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['product'].initial = self.instance.product.values_list('id', flat=True)
            self.fields['sector_label'].initial = self.instance.sector_label.values_list('id', flat=True)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['sector_label'].queryset = UniqueSector.objects.all()

    def save(self, commit=True):
        instance = super().save(commit=False)
        products = self.cleaned_data.get('product')
        sector_labels = self.cleaned_data.get('sector_label')
        
        if commit:
            instance.save()
            if products:
                instance.product.set(products)
            if sector_labels:
                instance.sector_label.set(sector_labels)
        return instance

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        name = cleaned_data.get("name")
        country = cleaned_data.get("country")
        province = cleaned_data.get("province")

        if category == 'individual' and Client.objects.filter(name=name, category='individual').exclude(pk=self.instance.pk).exists():
            self.add_error('name', f"Un client individuel avec le nom '{name}' existe déjà.")
        
        if category == 'enterprise' and Client.objects.filter(name=name, category='enterprise').exclude(pk=self.instance.pk).exists():
            self.add_error('name', f"Une entreprise avec le nom '{name}' existe déjà.")
        
        if country and country.country == 'Congo (Kinshasa)' and not province:
            self.add_error('province', "Le champ province est requis pour le pays Congo (Kinshasa).")
        
        return cleaned_data
from .models import Transaction, Product, Supplier, Client, Producer

from django.utils.translation import gettext_lazy as _

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = ['producer', 'product', 'type', 'supplier', 'client', 'price',
#                   'quantity', 'unit_of_measure', 'currency', 'tva_rate', 'photo']
#         widgets = {
#             'producer': forms.Select(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
#             }),
#             'product': forms.Select(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
#             }),
#             'type': forms.Select(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
#             }),
#             'supplier': forms.Select(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
#             }),
#             'client': forms.Select(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select'
#             }),
#             'price': forms.NumberInput(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input',
#                 'step': '0.01',
#                 'placeholder': 'Entrez le prix'
#             }),
#             'quantity': forms.NumberInput(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input',
#                 'step': '0.01',
#                 'placeholder': 'Entrez la quantité'
#             }),
#             'unit_of_measure': forms.Select(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-select',
#                 'placeholder': 'Sélectionnez l’unité de mesure'
#             }),
#             'currency': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input',
#                 'value': 'CDF',
#                 'readonly': 'readonly'
#             }),
#             'tva_rate': forms.NumberInput(attrs={
#                 'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input',
#                 'readonly': 'readonly',
#                 'placeholder': 'Entrez le taux de TVA'
#             }),
#             'photo': forms.ClearableFileInput(attrs={
#                 'class': 'block w-full text-sm text-gray-500 dark:text-gray-400',
#             }),
#         }

#     def __init__(self, *args, **kwargs):
#         producer = kwargs.pop('producer', None)  # Extraire 'producer' des arguments
#         super().__init__(*args, **kwargs)

#         # Définir 'type' par défaut comme 'sale'
#         self.fields['type'].initial = 'sale'
#         self.fields['tva_rate'].initial = 0.16

#         if producer:
#             # Filtrer les produits associés au producteur
#             self.fields['product'].queryset = Product.objects.filter(producer=producer).order_by('product_label')

#             # Filtrer les fournisseurs associés au producteur
#             self.fields['supplier'].queryset = Supplier.objects.filter(producer=producer).order_by('name')

#             # Filtrer les clients associés au producteur
#             self.fields['client'].queryset = Client.objects.filter(producer=producer).order_by('name')

#     def clean(self):
#         cleaned_data = super().clean()
#         transaction_type = cleaned_data.get('type')
#         supplier = cleaned_data.get('supplier')
#         client = cleaned_data.get('client')

#         if transaction_type == 'sale' and client is None:
#             self.add_error('client', "Un client doit être spécifié pour les transactions de vente.")
#         elif transaction_type == 'purchase' and supplier is None:
#             self.add_error('supplier', "Un fournisseur doit être spécifié pour les transactions d'achat.")

#         return cleaned_data

from django import forms
class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['producer', 'product', 'type', 'supplier', 'client', 'price', 'quantity', 'unit_of_measure', 'currency', 'tva_rate', 'photo']
        labels = {
            'product': 'Produit',
            'type': 'Type de transaction',
            'supplier': 'Fournisseur',
            'client': 'Client',
            'price': 'Prix',
            'quantity': 'Quantité',
            'unit_of_measure': 'Unité de mesure',
            'currency': 'Devise',
            'tva_rate': 'Taux de TVA',
            'photo': 'Photo',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm'}),
            'type': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm'}),
            'supplier': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm'}),
            'client': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm'}),
            'price': forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'step': '0.01', 'placeholder': 'Entrez le prix'}),
            'quantity': forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'step': '0.01', 'placeholder': 'Entrez la quantité'}),
            'unit_of_measure': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'placeholder': 'Sélectionnez l’unité de mesure'}),
            'currency': forms.TextInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'value': 'CDF', 'readonly': 'readonly'}),
            'tva_rate': forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'readonly': 'readonly'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'mt-1 block w-full text-sm text-gray-500'}),
        }

    def __init__(self, *args, **kwargs):
        producer = kwargs.pop('producer', None)
        super().__init__(*args, **kwargs)

        self.fields['type'].initial = 'sale'
        self.fields['tva_rate'].initial = 0.16  # Initialiser le taux de TVA
        self.fields['tva_rate'].widget.attrs['readonly'] = True

        if producer:
            self.fields['product'].queryset = Product.objects.filter(producer=producer).order_by('product_label')
            self.fields['supplier'].queryset = Supplier.objects.filter(producer=producer).order_by('name')
            self.fields['client'].queryset = Client.objects.filter(producer=producer).order_by('name')

        # Masquer le champ producer et le définir en lecture seule
        self.fields['producer'] = forms.ModelChoiceField(
            queryset=Producer.objects.filter(id=producer.id),
            initial=producer,
            widget=forms.HiddenInput()
        )
        self.producer_name = producer.company_name  # Stocker le nom du producteur pour l'afficher dans le template

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        supplier = cleaned_data.get('supplier')
        client = cleaned_data.get('client')

        if transaction_type == 'sale' and client is None:
            self.add_error('client', "Un client doit être spécifié pour les transactions de vente.")
        elif transaction_type == 'purchase' and supplier is None:
            self.add_error('supplier', "Un fournisseur doit être spécifié pour les transactions d'achat.")

        return cleaned_data

class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = ['producer', 'product', 'quantity', 'unit_of_measure']
        labels = {
            'product': 'Produit',
            'quantity': 'Quantité',
            'unit_of_measure': 'Unité de mesure',
        }
        widgets = {
            'product': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm'}),
            'quantity': forms.NumberInput(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'step': '0.01', 'placeholder': 'Entrez la quantité'}),
            'unit_of_measure': forms.Select(attrs={'class': 'mt-1 block w-full border border-gray-300 rounded-md shadow-sm', 'placeholder': 'Sélectionnez l’unité de mesure'}),
        }

    def __init__(self, *args, **kwargs):
        producer = kwargs.pop('producer', None)
        super().__init__(*args, **kwargs)

        if producer:
            self.fields['product'].queryset = Product.objects.filter(producer=producer).order_by('product_label')

        # Masquer le champ producer et le définir en lecture seule
        self.fields['producer'] = forms.ModelChoiceField(
            queryset=Producer.objects.filter(id=producer.id),
            initial=producer,
            widget=forms.HiddenInput()
        )
        self.producer_name = producer.company_name  # Stocker le nom du producteur pour l'afficher dans le template

    def clean(self):
        cleaned_data = super().clean()
        
        return cleaned_data

class FilterForm(forms.Form):
    date_filter = forms.ChoiceField(
        choices=(
            ('', 'Tous'),
            ('today', "Aujourd'hui"),
            ('month', 'Ce Mois'),
            ('year', 'Cette Année'),
        ),
        required=False,
        label='Filtrer par Date'
    )
    product = forms.ModelChoiceField(
        queryset=Product.objects.all(),
        required=False,
        label='Filtrer par Produit'
    )
    producer = forms.ModelChoiceField(
        queryset=Producer.objects.all(),
        required=False,
        label='Filtrer par Producteur'
    )

class DateFilterForm(forms.Form):
    date_filter = forms.ChoiceField(choices=[
        ('', 'Tous les temps'),
        ('today', "Aujourd'hui"),
        ('month', 'Ce mois-ci'),
        ('year', 'Cette année')
    ], required=False)

class ProductFilterForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), empty_label="Tous les produits", required=False)

class ProducerFilterForm(forms.Form):
    producer = forms.ModelChoiceField(queryset=Producer.objects.all(), empty_label="Tous les producteurs", required=False)

# class ProductMatrixFilterForm(forms.Form):
#     product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label='Sélectionner un produit')
#     matrix_type = forms.ChoiceField(choices=[('quantity', 'Quantité'), ('price', 'Prix')], required=True, label='Type de matrice')

class ProductMatrixFilterForm(forms.Form):
    product = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label='Sélectionner un produit')
    matrix_type = forms.ChoiceField(choices=[('quantity', 'Quantité'), ('price', 'Prix')], required=True, label='Type de matrice')
