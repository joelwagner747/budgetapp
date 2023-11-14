from django.forms import ModelForm
from .models import Transaction, Budget, Category


class CreateTransactionForm(ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Filter the choices for the budget field based on user's budgets
        if user:
            self.fields["budget"].queryset = Budget.objects.filter(user=user)

    class Meta:
        model = Transaction
        fields = [
            "budget",
            "merchant",
            "amount",
            "category",
            "date",
        ]


class CreateCategoryForm(ModelForm):
    class Meta:
        model = Category
        fields = [
            "name",
            "amount_budgeted",
        ]
