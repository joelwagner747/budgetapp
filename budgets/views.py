from typing import Any
from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView
from django.urls import reverse
from .models import Transaction, Budget, Income, Category


class CreateTransaction(CreateView):
    model = Transaction
    template_name = "add_transaction.html"
    fields = [
        "merchant",
        "amount",
        "date",
        "category",
    ]

    def get_success_url(self):
        return self.request.GET.get("next", reverse("home"))


class UserHomeView(ListView):
    model = Budget
    template_name = "user_home.html"
    queryset = Budget.objects.order_by("date")


class BudgetView(DetailView):
    model = Budget
    template_name = "budget_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income = self.object.income_set.all()
        if len(income) > 0:
            context["income"] = self.object.income_set.all()[0]
        else:
            context["income"] = 0
        context["categories"] = self.object.category_set.all().order_by("name")
        return context


class CatagoryDetail(DetailView):
    model = Category
    template_name = "category_detail.html"
