from django import forms

from .models import Cryptocurrencies


class PostForm(forms.ModelForm):

    class Meta:
        model = Cryptocurrencies
        fields = ('identificator', 'symbols', 'value', 'is_crypto',)
