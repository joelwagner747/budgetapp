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
    CatagoryDetail,
    CategoryEditView,
    CategoryDeleteView,
    SetIncome,
    DeleteTransactionView,
    EditTransactionView,
    TransactionView,
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
    path("<int:pk>/category/", CatagoryDetail.as_view(), name="category_detail"),
    path("<int:pk>/edit_category/", CategoryEditView.as_view(), name="category_edit"),
    path(
        "<int:pk>/delete_category/",
        CategoryDeleteView.as_view(),
        name="category_delete",
    ),
    path("<int:pk>/set_income/", SetIncome.as_view(), name="set_income"),
    path(
        "<int:pk>/delete_transaction/",
        DeleteTransactionView.as_view(),
        name="delete_transaction",
    ),
    path(
        "<int:pk>/edit_transaction/",
        EditTransactionView.as_view(),
        name="edit_transaction",
    ),
    path(
        "<int:pk>/transactions/", TransactionView.as_view(), name="budget_transactions"
    ),
]
