# Generated by Django 4.2.7 on 2023-12-13 03:52

import datetime
from decimal import Decimal
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import djmoney.models.fields


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Budget",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                ("date", models.DateTimeField(auto_now_add=True)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Category",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=255)),
                (
                    "amount_budgeted_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "US Dollar")],
                        default="USD",
                        editable=False,
                        max_length=3,
                        null=True,
                    ),
                ),
                (
                    "amount_budgeted",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2,
                        default_currency="USD",
                        max_digits=14,
                        null=True,
                    ),
                ),
                (
                    "budget",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="budgets.budget"
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Transaction",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("merchant", models.CharField(max_length=255)),
                (
                    "amount_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "US Dollar")],
                        default="USD",
                        editable=False,
                        max_length=3,
                    ),
                ),
                (
                    "amount",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2, default_currency="USD", max_digits=14
                    ),
                ),
                ("date", models.DateField(default=datetime.date.today)),
                (
                    "budget",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="budgets.budget"
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="budgets.category",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Income",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "monthly_income_currency",
                    djmoney.models.fields.CurrencyField(
                        choices=[("USD", "US Dollar")],
                        default="USD",
                        editable=False,
                        max_length=3,
                        null=True,
                    ),
                ),
                (
                    "monthly_income",
                    djmoney.models.fields.MoneyField(
                        decimal_places=2,
                        default=Decimal("0"),
                        default_currency="USD",
                        max_digits=14,
                        null=True,
                    ),
                ),
                (
                    "budget",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="budgets.budget"
                    ),
                ),
            ],
        ),
    ]
