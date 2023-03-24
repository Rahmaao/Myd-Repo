from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from core import models
from django import forms, http
from core.forms import *
from django.views.generic.edit import FormView


# def category_list(request):
#     if request.method == "POST":
#         addcategory = request.POST["categoryname"]
#         models.Category.objects.create(name=addcategory, age=)
#     categories = models.Category.objects.all()
#     # for category in categories:
#     #     print (category.product_count)
#     context = {"categories": categories}
#     return render(request, "categories.html", context)


def delete_category(request, pk):
    category = Category.objects.get(pk=pk)
    # category.created_by = self.request.user
    category.delete()
    return redirect(
        reverse("category-list")
    )  # redirect to the original page (which is named in the urls.py) after deleting


# def update_category(request, pk):
#     category = get_object_or_404(models.Category, pk=pk)
#     if request.method == "POST":
#         category_name = request.POST["categoryname"]
#         category.name = category_name  # the item you have gotten .model field will be changed to what was given in th epost request
#         category.save()        
#         return redirect(
#             reverse("categories")
#         )  # name of url to redirect to after updating is complete
#     return render(
#         request, "update.html", {"category": category}
#     )  # the original template that will be shown once an update operation is initiated


# def category_details(request, pk):
#     if request.method == "POST":
#         productname = request.POST["productname"]
#         description = request.POST["description"]
#         sku = request.POST["sku"]
#         discount = request.POST["discount"]
#         if discount == "":
#             discount = 0
#         stock = request.POST["stock"]
#         product_price = request.POST["product_price"]
#         color = request.POST["color"]
#         size = request.POST["size"]
#         manufacturer = request.POST["manufacturer"]
#         brand = request.POST["brand"]
#         dimension = request.POST["dimension"]
#         weight = request.POST["weight"]
#         # is_available = request.POST["is_available"]  # new var is equal to the post request as the var is saved in the html
#         thiscategory = models.Category.objects.get(
#             pk=pk
#         )  # set new todo in particular category where pk is equal to the current pk (pk of the category)
#         models.Product.objects.create(
#             name=productname,
#             description=description,
#             sku=sku,
#             discount=discount,
#             stock=stock,
#             product_price=product_price,
#             color=color,
#             size=size,
#             manufacturer=manufacturer,
#             brand=brand,
#             dimension=dimension,
#             weight=weight,
#             # is_available=is_available,
#             category=thiscategory,
#         )  # the model field is equal to the variables in the view function above
#     productcategory = get_object_or_404(models.Category, pk=pk)
#     productlist = models.Product.objects.filter(
#         category=productcategory
#     )  # filter using the fk in the model , category, i guess
#     context = {"productcategory": productcategory, "productlist": productlist}
#     return render(request, "category.html", context)


class CategoryListView(ListView):
    model = Category
    context_object_name = 'categories'


class CategoryDetailView(DetailView):
    model = Category
    context_object_name = 'category'


class CategoryCreateView(CreateView):
    model = Category
    fields = '__all__'

    def get_success_url(self):
        return reverse('category-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        obj.save()
        print(obj.created_by)
        return http.HttpResponseRedirect(self.get_success_url())


class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['name']

    def get_success_url(self):
        return reverse('category-list')

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.created_by == self.request.user:
            obj.save()
        else:
            print("You cant update")
        return http.HttpResponseRedirect(self.get_success_url())

# class PlaceFormView(CreateView):
#     form_class = PlaceForm

#     @method_decorator(login_required)
#     def dispatch(self, *args, **kwargs):
#         return super(PlaceFormView, self).dispatch(*args, **kwargs)

#     def form_valid(self, form):
#         obj = form.save(commit=False)
#         obj.created_by = self.request.user
#         obj.save()        
#         return http.HttpResponseRedirect(self.get_success_url())


# def get_context_data(self, **kwargs):
#     # Call the base implementation first to get a context
#     context = super().get_context_data(**kwargs)
#     # Add in a QuerySet of all the books
#     context['product_list'] = Product.objects.all()
#     return context
