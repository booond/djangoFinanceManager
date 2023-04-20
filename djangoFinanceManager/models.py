from django.db import models


class Cryptocurrencies(models.Model):
    class Meta:
        app_label = 'djangoFinanceManager'

    identificator = models.CharField(max_length=32, default=None)
    symbols = models.CharField(max_length=10)
    value = models.DecimalField(max_digits=20, decimal_places=10)
    last_updated = models.DateTimeField(auto_now=True)
    is_crypto = models.BooleanField()

    def __str__(self):
        return f'{self.symbols} ({self.identificator}) — {float(self.value):g}'


class History(models.Model):
    class Meta:
        app_label = 'djangoFinanceManager'

    crypto_currency = models.ForeignKey(Cryptocurrencies, on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    amount = models.DecimalField(max_digits=20, decimal_places=10)
    date = models.DateTimeField(auto_now_add=True)
