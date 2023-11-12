from django.urls import path
from .views import BudgetView, UserHomeView, AddTransactionView, GetCategoriesView

urlpatterns = [
    path("", UserHomeView.as_view(), name="user_home"),
    path("budget<int:pk>/", BudgetView.as_view(), name="budget"),
    path("add_transaction/", AddTransactionView.as_view(), name="add_transaction"),
    path("get_categories/", GetCategoriesView.as_view(), name="get_categories"),
]
