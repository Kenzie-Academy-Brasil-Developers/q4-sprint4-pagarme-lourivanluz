from rest_framework.urls import path


from payables.views import PayablesView

urlpatterns = [path("payables/", PayablesView.as_view())]
