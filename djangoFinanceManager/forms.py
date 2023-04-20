from django import forms

from .models import Cryptocurrencies


class PostForm(forms.ModelForm):

    class Meta:
        model = Cryptocurrencies

        exclude = ('symbols',)
        fields = ('identificator', 'value', 'is_crypto',)
