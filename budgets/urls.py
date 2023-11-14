from django.urls import path
from .views import (
    BudgetView,
    UserHomeView,
    AddTransactionView,
    GetCategoriesView,
    HomeView,
    AddBudgetView,
    BudgetEditView,
    BudgetDeleteView,
)

urlpatterns = [
    path("user/", UserHomeView.as_view(), name="user_home"),
    path("budget<int:pk>/", BudgetView.as_view(), name="budget"),
    path("add_transaction/", AddTransactionView.as_view(), name="add_transaction"),
    path("get_categories/", GetCategoriesView.as_view(), name="get_categories"),
    path("", HomeView.as_view(), name="home"),
    path("add_budget/", AddBudgetView.as_view(), name="add_budget"),
    path("<int:pk>/edit_budget/", BudgetEditView.as_view(), name="budget_edit"),
    path("<int:pk>/delete_budget/", BudgetDeleteView.as_view(), name="budget_delete"),
]
