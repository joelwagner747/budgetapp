from typing import Any
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from django.views.generic import DetailView, ListView, View
from django.urls import reverse_lazy
from django.http import JsonResponse, HttpResponseRedirect
from .models import Transaction, Budget, Income, Category
from .forms import CreateTransactionForm


class AddTransactionView(View):
    template_name = "add_transaction.html"

    def get(self, request, *args, **kwargs):
        form = CreateTransactionForm()
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateTransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse_lazy("user_home")
            )  # Redirect to success page
        return render(request, self.template_name, {"form": form})

    """def get_success_url(self):
        return reverse("user_home")"""


class GetCategoriesView(View):
    def get(self, request, *args, **kwargs):
        budget_id = request.GET.get("budget_id")
        categories = Category.objects.filter(budget_id=budget_id)
        category_list = [
            {"id": category.id, "name": category.name} for category in categories
        ]
        return JsonResponse(category_list, safe=False)


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
