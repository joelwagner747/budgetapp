# Generated by Django 4.2.7 on 2023-11-02 23:28

from django.db import migrations
import django_countries.fields


class Migration(migrations.Migration):
    dependencies = [
        ("accounts", "0001_initial"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="customuser",
            name="city",
        ),
        migrations.AlterField(
            model_name="customuser",
            name="country",
            field=django_countries.fields.CountryField(
                blank=True, max_length=2, null=True
            ),
        ),
    ]