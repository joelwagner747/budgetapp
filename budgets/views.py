from typing import Any
from django.shortcuts import render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import DetailView, ListView, View, TemplateView, FormView
from django.urls import reverse_lazy, reverse
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse, HttpResponseRedirect
from djmoney.money import Money
from .models import Transaction, Budget, Income, Category
from .forms import CreateTransactionForm, CreateCategoryForm, UpdateTransactionForm


class AddTransactionView(LoginRequiredMixin, View):
    template_name = "add_transaction.html"

    def get(self, request, *args, **kwargs):
        form = CreateTransactionForm(user=request.user)
        return render(request, self.template_name, {"form": form})

    def post(self, request, *args, **kwargs):
        form = CreateTransactionForm(request.POST, user=request.user)
        if form.is_valid():
            transaction = form.save(commit=False)
            if transaction.category.budget != transaction.budget:
                # Handle the case where the category and budget don't match
                # You might want to display an error message or take appropriate action
                return render(
                    request,
                    self.template_name,
                    {
                        "form": form,
                        "error": "Category does not belong to the selected budget.",
                    },
                )

            transaction.save()
            return HttpResponseRedirect(reverse_lazy("user_home"))
        return render(request, self.template_name, {"form": form})


class GetCategoriesView(LoginRequiredMixin, View):
    def get(self, request, *args, **kwargs):
        form = CreateCategoryForm()  # Instantiate the form
        budget_id = request.GET.get("budget_id")
        categories = Category.objects.filter(budget_id=budget_id)
        category_list = [
            {"id": category.id, "name": category.name} for category in categories
        ]
        return JsonResponse(category_list, safe=False)


class UserHomeView(LoginRequiredMixin, ListView):
    model = Budget
    template_name = "user_home.html"

    def get_queryset(self):
        budgets = Budget.objects.filter(user=self.request.user).order_by("-date")
        for budget in budgets:
            income = budget.income_set.all()
            budget.income = income[0]
            categories = budget.category_set.all().order_by("name")
            total = 0
            for category in categories:
                transactions = Transaction.objects.filter(category=category)
                amount = 0
                for transaction in transactions:
                    amount += transaction.amount
                if amount == 0:
                    category.amount_spent = Money(amount, "USD")
                else:
                    category.amount_spent = amount
                total += amount
            if total == 0:
                total = Money(total, "USD")
            budget.categories = categories
            budget.total = total

        return budgets


class BudgetGet(UserPassesTestMixin, DetailView):
    model = Budget
    template_name = "budget_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        income = self.object.income_set.all()
        print(income)
        context["income"] = income[0]
        categories = self.object.category_set.all().order_by("name")
        total = 0
        for category in categories:
            transactions = Transaction.objects.filter(category=category)
            amount = 0
            for transaction in transactions:
                amount += transaction.amount
            if amount == 0:
                category.amount_spent = Money(amount, "USD")
            else:
                category.amount_spent = amount
            total += amount
        if total == 0:
            total = Money(total, "USD")
        context["total_spent"] = total
        context["categories"] = categories
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BudgetPost(UserPassesTestMixin, SingleObjectMixin, FormView):
    model = Budget
    form_class = CreateCategoryForm
    template_name = "budget_detail.html"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        category = form.save(commit=False)
        category.budget = self.object
        category.save()
        return super().form_valid(form)

    def get_success_url(self):
        budget = self.object
        return reverse("budget", kwargs={"pk": budget.pk})

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BudgetView(LoginRequiredMixin, DetailView):
    def get(self, request, *args, **kwargs):
        view = BudgetGet.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = BudgetPost.as_view()
        return view(request, *args, **kwargs)

    """def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user"""


class CatagoryDetail(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Category
    template_name = "category_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        transactions = self.object.transaction_set.all().order_by("date")
        context["transactions"] = transactions
        amount = 0
        for transaction in transactions:
            amount += transaction.amount

        if amount == 0:
            self.object.amount_spent = Money(amount, "USD")
        else:
            self.object.amount_spent = amount
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.budget.user == self.request.user


class HomeView(TemplateView):
    template_name = "home.html"


class BudgetEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Budget
    fields = ("name",)
    template_name = "budget_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class BudgetDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Budget
    template_name = "budget_delete.html"
    success_url = reverse_lazy("user_home")

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user


class AddBudgetView(LoginRequiredMixin, CreateView):
    model = Budget
    template_name = "add_budget.html"
    fields = ("name",)

    def form_valid(self, form):
        form.instance.user = self.request.user
        respone = super().form_valid(form)
        income = Income.objects.create(
            budget=form.instance,
        )
        return respone


class CategoryEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Category
    fields = (
        "name",
        "amount_budgeted",
    )
    template_name = "category_edit.html"

    def test_func(self):
        obj = self.get_object()
        return obj.budget.user == self.request.user


class CategoryDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Category
    template_name = "category_delete.html"

    def get_success_url(self):
        return reverse("budget", kwargs={"pk": self.object.budget_id})

    def test_func(self):
        obj = self.get_object()
        return obj.budget.user == self.request.user


class SetIncome(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Income
    fields = ("monthly_income",)
    template_name = "income_set.html"

    def get_success_url(self):
        return reverse("budget", kwargs={"pk": self.object.budget_id})

    def test_func(self):
        obj = self.get_object()
        return obj.budget.user == self.request.user


class DeleteTransactionView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Transaction
    template_name = "transaction_delete.html"

    def get_success_url(self):
        return reverse("category_detail", kwargs={"pk": self.object.category_id})

    def test_func(self):
        obj = self.get_object()
        return obj.budget.user == self.request.user


class EditTransactionView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Transaction
    form_class = UpdateTransactionForm
    template_name = "transaction_edit.html"

    def form_valid(self, form):
        # Add custom logic if needed
        return super().form_valid(form)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        # Add any additional kwargs if needed
        return kwargs

    def get_success_url(self):
        return reverse("category_detail", kwargs={"pk": self.object.category_id})

    def test_func(self):
        obj = self.get_object()
        return obj.budget.user == self.request.user


class TransactionView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Budget
    template_name = "transactions.html"

    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        transactions = self.object.transaction_set.all().order_by("merchant")
        context["transactions"] = transactions
        return context

    def test_func(self):
        obj = self.get_object()
        return obj.user == self.request.user
