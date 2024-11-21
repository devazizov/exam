from django.views.generic import TemplateView, CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth import update_session_auth_hash
from django.views import View
from django.http import Http404
from django.contrib.auth import get_user_model
from django.urls import reverse_lazy, reverse

from .forms import RegistrationForm, AccountForm
from main.models import Product, Cart

User = get_user_model()


class RegistrationPage(CreateView):
    template_name = "registration/registration.html"
    model = User
    form_class = RegistrationForm
    success_url = reverse_lazy("login")
    extra_context = {"is_registration": True}


class AccountPage(LoginRequiredMixin, UpdateView):
    template_name = "users/account.html"
    model = User
    form_class = AccountForm
    pk_url_kwarg = "user_id"

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        if obj != self.request.user:
            raise Http404
        return obj

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["is_profile"] = True
        return context

    def form_valid(self, form):
        password1 = form.cleaned_data.get("password1")

        if password1:
            self.object.set_password(password1)
            self.object.save()
            update_session_auth_hash(self.request, self.object)

        return super().form_valid(form)

    def get_success_url(self):
        if self.request.user.is_authenticated:
            return reverse("profile", kwargs={"user_id": self.request.user.id})
        else:
            return reverse("login")


class CartPage(LoginRequiredMixin, TemplateView):

    def get(self, request):
        context = {
            "is_cart": True,
            "carts": request.user.cart_set.all(),
            "products": Product.objects.all(),
        }
        if request.user.is_authenticated:
            context["cart_product_quantity"] = request.user.cart_set.count()

        return render(request, template_name="users/cart.html", context=context)


def logout_page(request):
    logout(request)
    return redirect("login")


class CartProductDelete(LoginRequiredMixin, DeleteView):
    model = Cart
    success_url = reverse_lazy("home")
    pk_url_kwarg = "cart_product_id"


class IncrementView(LoginRequiredMixin, View):
    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        cart.quantity += 1
        cart.save()
        return redirect("cart")


class DecrementView(LoginRequiredMixin, View):
    def post(self, request, cart_id):
        cart = get_object_or_404(Cart, id=cart_id)
        if cart.quantity > 1:
            cart.quantity -= 1
        cart.save()
        return redirect("cart")
