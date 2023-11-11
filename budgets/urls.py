from django.urls import path
from .views import BudgetView, UserHomeView, CreateTransaction

urlpatterns = [
    path("", UserHomeView.as_view(), name="user_home"),
    path("budget<int:pk>/", BudgetView.as_view(), name="budget"),
    path("add_transaction/", CreateTransaction.as_view(), name="add_transaction"),
]
