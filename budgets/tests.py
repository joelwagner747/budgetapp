from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from djmoney.money import Money
from .models import Budget, Category, Transaction, Income

# Create your tests here.


class BudgetTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(
            username="testuser", email="test@email.com", password="secret"
        )
        cls.budget = Budget.objects.create(name="Test", user=cls.user)
        cls.category = Category.objects.create(
            budget=cls.budget, name="TestCategory", amount_budgeted=Money(200, "USD")
        )
        cls.income = Income.objects.create(
            budget=cls.budget, monthly_income=Money(2000, "USD")
        )

    def test_create_budget(self):
        budget = Budget.objects.create(name="Test2", user=self.user)
        self.assertEqual(budget.name, "Test2")
        self.assertEqual(budget.user, self.user)

    def test_create_category(self):
        category = Category.objects.create(
            budget=self.budget, name="TestCategory2", amount_budgeted=Money(400, "USD")
        )
        self.assertEqual(category.budget, self.budget)
        self.assertEqual(category.name, "TestCategory2")
        self.assertEqual(category.amount_budgeted, Money(400, "USD"))

    def test_create_transaction(self):
        transaction = Transaction.objects.create(
            merchant="Test Merchant",
            amount=Money(24.99, "USD"),
            category=self.category,
            budget=self.budget,
        )
        self.assertEqual(transaction.merchant, "Test Merchant")
        self.assertEqual(transaction.amount, Money(24.99, "USD"))
        self.assertEqual(transaction.category, self.category)
        self.assertEqual(transaction.budget, self.budget)

    def test_create_income(self):
        income = Income.objects.create(
            budget=self.budget, monthly_income=Money(2000, "USD")
        )
        self.assertEqual(income.budget, self.budget)
        self.assertEqual(income.monthly_income, Money(2000, "USD"))

    def test_add_budget(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.post(
            reverse("add_budget"),
            data={"name": "New Budget"},
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Budget.objects.last().name, "New Budget")
        self.assertEqual(Budget.objects.last().user, self.user)

    def test_add_category(self):
        self.client.login(username="testuser", password="secret")
        response = self.client.post(
            reverse("budget", kwargs={"pk": self.budget.id}),
            data={"name": "Test Category1", "amount_budgeted": 100.0},
        )
        print(Category.objects.all())
        self.assertEqual(response.status_code, 302)
        # self.assertEqual(Category.objects.last().name, "Test Category1")
        # self.assertEqual(Category.objects.last().amount_budgeted, Money(100, "USD"))
