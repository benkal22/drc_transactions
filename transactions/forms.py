from django import forms
from .models import Supplier, Producer, Product, Province
from .models import Client
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class ProducerForm(forms.ModelForm):
    class Meta:
        model = Producer
        fields = '__all__'
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
            if isinstance(field.widget, forms.widgets.CheckboxInput):
                field.widget.attrs.update({'class': 'form-check-input'})
            if isinstance(field.widget, forms.widgets.FileInput):
                field.widget.attrs.update({'class': 'form-control-file'})
