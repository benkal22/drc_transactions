# forms.py

from django import forms
from allauth.account.forms import LoginForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit, Div

class CrispyLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-control'  # Ajoutez des classes Bootstrap ou personnalisées au formulaire
        self.helper.layout = Layout(
            Div(
                'login',
                'password',
                Submit('submit', 'Connexion', css_class='btn btn-primary mt-3 w-100'),
                css_class='mb-3'
            )
        )
