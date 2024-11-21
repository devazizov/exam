from django.urls import path
from django.contrib.auth.views import LoginView

from . import views
from .forms import LoginForm

urlpatterns = [
    path(
        "login/",
        LoginView.as_view(extra_context={"is_login": True}, form_class=LoginForm),
        name="login",
    ),
    path("registration/", views.RegistrationPage.as_view(), name="registration"),
    path("logout/", views.logout_page, name="logout"),
    path("account/<int:user_id>/", views.AccountPage.as_view(), name="profile"),
    path("cart/", views.CartPage.as_view(), name="cart"),
        path(
        "cart_product_detele/<int:cart_product_id>/",
        views.CartProductDelete.as_view(),
        name="cart_product_delete",
    ),
    path(
        "cart/increment/<int:cart_id>/",
        views.IncrementView.as_view(),
        name="increment_quantity",
    ),
    path(
        "cart/decrement/<int:cart_id>/",
        views.DecrementView.as_view(),
        name="decrement_quantity",
    ),
]
