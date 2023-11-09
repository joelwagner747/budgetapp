from django.db import models
from djmoney.models.fields import MoneyField
from datetime import date
from django.urls import reverse
from django.conf import settings

# Create your models here.


class Category(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    name = models.CharField(max_length=255)
    amount_budgeted = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        null=True,
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("catagory_detail", kwargs={"pk": self.pk})


class Transaction(models.Model):
    merchant = models.CharField(max_length=255)
    amount = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
    )
    Date = models.DateField(default=date.today)
    catagory = models.ForeignKey(
        "Category",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"{self.merchant} {self.amount}"


class Income(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
    )
    monthly_income = MoneyField(
        max_digits=14,
        decimal_places=2,
        default_currency="USD",
        null=True,
    )

    def __str__(self):
        return str(self.monthly_income)
