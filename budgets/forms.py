from django.forms import ModelForm
from .models import Transaction, Budget, Category


class CreateTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = [
            "budget",
            "merchant",
            "amount",
            "category",
            "date",
        ]
