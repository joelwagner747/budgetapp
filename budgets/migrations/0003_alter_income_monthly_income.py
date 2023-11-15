# Generated by Django 4.2.7 on 2023-11-14 20:39

from decimal import Decimal
from django.db import migrations
import djmoney.models.fields


class Migration(migrations.Migration):
    dependencies = [
        ("budgets", "0002_alter_category_amount_budgeted_currency_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="income",
            name="monthly_income",
            field=djmoney.models.fields.MoneyField(
                decimal_places=2,
                default=Decimal("0"),
                default_currency="USD",
                max_digits=14,
                null=True,
            ),
        ),
    ]