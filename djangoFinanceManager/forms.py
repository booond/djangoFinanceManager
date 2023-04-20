from django import forms

from .models import Cryptocurrencies, History


class PostForm(forms.ModelForm):

    class Meta:
        model = Cryptocurrencies

        exclude = ('symbols',)
        fields = ('identificator', 'value', 'is_crypto',)


class HistoryForm(forms.ModelForm):
    TYPES = (
        ('income', 'Дохід'),
        ('expense', 'Витрата'),
    )

    type = forms.ChoiceField(choices=TYPES, label='Тип')
    crypto_currency = forms.ModelChoiceField(queryset=Cryptocurrencies.objects.all(), label='Валюта')
    amount = forms.DecimalField(label='Кількість')

    class Meta:
        model = History
        fields = ['type', 'crypto_currency', 'amount']
