from rest_framework.urls import path
from fees.views import FeesView, FeesViewId

urlpatterns = [
    path("fee/", FeesView.as_view()),
    path("fee/<str:pk>/", FeesViewId.as_view()),
]
