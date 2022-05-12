from rest_framework.urls import path


from payment_info.views import PaymentesInfoView


urlpatterns = [
    path('payment_info/',PaymentesInfoView.as_view())
]