from django.forms import ModelForm, TextInput
from .models import City
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CityForm(ModelForm):
    helper = FormHelper()
    helper.form_show_labels = False

    class Meta:
        model = City
        fields = ['name']
        widgets = {'name': TextInput(attrs={'class': 'input', 'placeholder': 'City Name'})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Save person'))
