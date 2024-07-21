from django import forms
from .models import Supplier, Producer, Client, Transaction, Product, UniqueSector
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.utils import timezone
from django import forms
from .models import Supplier, Product, UniqueSector, Country, Province

# class ProducerForm(forms.ModelForm):
#     class Meta:
#         model = Producer
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class': 'form-control'})
#             if isinstance(field.widget, forms.widgets.CheckboxInput):
#                 field.widget.attrs.update({'class': 'form-check-input'})
#             if isinstance(field.widget, forms.widgets.FileInput):
#                 field.widget.attrs.update({'class': 'form-control-file'})

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

# class TransactionForm(forms.ModelForm):
#     class Meta:
#         model = Transaction
#         fields = '__all__'
    
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         for field in self.fields.values():
#             field.widget.attrs.update({'class': 'form-control'})
#             if isinstance(field.widget, forms.widgets.CheckboxInput):
#                 field.widget.attrs.update({'class': 'form-check-input'})
#             if isinstance(field.widget, forms.widgets.FileInput):
#                 field.widget.attrs.update({'class': 'form-control-file'})

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = [
            'producer', 'product', 'type', 'supplier', 'client',
            'price', 'quantity', 'unit_of_measure', 'currency'
        ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['type'].initial = 'sale'
        self.fields['producer'].widget.attrs.update({
            'id': 'id_producer',
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
        })
        self.fields['product'].queryset = Product.objects.none()
        self.fields['product'].widget.attrs.update({
            'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
        })

        if 'producer' in self.data:
            try:
                producer_id = int(self.data.get('producer'))
                self.fields['product'].queryset = Product.objects.filter(producer__id=producer_id).order_by('product_label')
                self.fields['supplier'].queryset = Supplier.objects.filter(producersupplier__producer__id=producer_id).order_by('name')
                self.fields['client'].queryset = Client.objects.filter(producerclient__producer__id=producer_id).order_by('name')
            except (ValueError, TypeError):
                pass  # Invalid input from the client; ignore and fallback to empty querysets
        elif self.instance.pk:
            self.fields['product'].queryset = self.instance.producer.product.all().order_by('product_label')
            self.fields['supplier'].queryset = self.instance.producer.suppliers.order_by('name')
            self.fields['client'].queryset = self.instance.producer.clients.order_by('name')

        for field_name in self.fields:
            self.fields[field_name].widget.attrs.update({
                'class': 'block w-full mt-1 text-sm dark:text-gray-300 dark:border-gray-600 dark:bg-gray-700 focus:border-purple-400 focus:outline-none focus:shadow-outline-purple dark:focus:shadow-outline-gray form-input'
            })

    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        supplier = cleaned_data.get('supplier')
        client = cleaned_data.get('client')

        if transaction_type == 'sale':
            if client is None:
                self.add_error('client', "Client must be specified for sales transactions.")
        elif transaction_type == 'purchase':
            if supplier is None:
                self.add_error('supplier', "Supplier must be specified for purchase transactions.")

        return cleaned_data

    def get_date(self):
        date_option = self.cleaned_data.get('date_option')
        date_manual = self.cleaned_data.get('date_manual')

        if date_option == 'now':
            return timezone.now()
        elif date_option == 'manual':
            return date_manual
        return None


# class ClientForm(forms.ModelForm):
#     class Meta:
#         model = Client
#         fields = [
#             'category', 'name', 'manager_name', 'tax_code', 'nrc',
#             'nat_id', 'address', 'email', 'phone_number',
#             'country', 'province', 'product', 'sector_label', 'photo'
#         ]
#         widgets = {
#             'category': forms.Select(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'manager_name': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'tax_code': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'nrc': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'nat_id': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'name': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'address': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'email': forms.EmailInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'phone_number': forms.TextInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'country': forms.Select(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'province': forms.Select(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'product': forms.SelectMultiple(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'sector_label': forms.SelectMultiple(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#             'photo': forms.ClearableFileInput(attrs={
#                 'class': 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm'
#             }),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Ajouter une classe pour une meilleure lisibilité en mode paysage
#         self.fields['address'].widget.attrs['class'] = 'block w-full mt-1 p-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm h-24 overflow-auto'

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
