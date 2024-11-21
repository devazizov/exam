from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Category, Product, Cart


class HomePage(ListView):
    model = Product
    template_name = "main/home.html"
    context_object_name = "products"
    paginate_by = 6
    extra_context = {"is_home": True}

    def get_queryset(self):
        search_term = self.request.GET.get("search", "")
        if search_term:
            return Product.objects.filter(
                title__icontains=search_term
        ).order_by("-id")
        else:
            return Product.objects.all().order_by("-id")



class CategoryListView(ListView):
    model = Category
    template_name = "main/categories.html"
    context_object_name = "categories"
    extra_context = {"is_category": True}

class ProductListView(ListView):
    model = Product
    template_name = "main/product_list.html"
    context_object_name = "products"
    paginate_by = 6 

    def get_queryset(self):
        category_id = self.kwargs.get("category_id")
        return Product.objects.filter(category_id=category_id)


@login_required(login_url="login")
def add_to_cart(request, product_id):
    if request.method == "POST":
        user = request.user
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        try:
            cart_item = Cart.objects.get(user=user, product=product)
            cart_item.quantity += quantity
            cart_item.save()
            messages.success(request, "Product added to cart!")
        except Cart.DoesNotExist:
            Cart.objects.create(
                product=product,
                user=user,
                quantity=quantity,
            )
            messages.success(request, "Product added to cart!")

    else:
        messages.error(request, "Invalid request!")

    return redirect(request.META.get("HTTP_REFERER", "home"))
