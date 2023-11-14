from django.contrib import admin
from .models import Category, Transaction, Income, Budget

# Register your models here.
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(Income)
admin.site.register(Budget)
