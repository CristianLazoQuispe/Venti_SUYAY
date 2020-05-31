from django.contrib.auth.views import LoginView,LogoutView
from django.urls import path
from django.views.generic.base import TemplateView
from django.contrib.auth.decorators import login_required
from .views import Dashboard, AmbientesAjax
urlpatterns = [
    path("dashboard", login_required(Dashboard.as_view()), name="dashboard"),
    path("ajax/ambiente", AmbientesAjax.as_view(), name="ajaxAmbiente"),
    path("login", LoginView.as_view(template_name="login.html"), name="login"),
    path("logout", LoginView.as_view(template_name="logged_out.html"), name="logout"),
]