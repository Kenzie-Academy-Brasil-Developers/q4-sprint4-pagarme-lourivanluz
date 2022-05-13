from rest_framework.urls import path


from transactions.views import TransactionsView

urlpatterns = [
    path("transactions/", TransactionsView.as_view(), name="createTransaction"),
]
