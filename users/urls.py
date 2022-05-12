from rest_framework.urls import path


from users.views import UsersView, LoginView

urlpatterns = [
    path("accounts/", UsersView.as_view()),
    path("login/", LoginView.as_view()),
]
