from django.forms import ModelForm
from djmoney.forms.fields import MoneyField
from .models import Transaction, Budget, Category, Income


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


class CreateIncomeForm(ModelForm):
    class Meta:
        model = Income
        fields = ["monthly_income"]

    monthly_income = MoneyField(required=False)


class UpdateTransactionForm(ModelForm):
    class Meta:
        model = Transaction
        fields = ["merchant", "category", "amount"]  # Add other fields as needed

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Dynamically filter the choices for the category field
        instance = kwargs.get("instance")
        if instance:
            budget = instance.category.budget
            self.fields["category"].queryset = Category.objects.filter(budget=budget)
