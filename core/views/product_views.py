from django.shortcuts import redirect, render
from django.urls import reverse
from core import models
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from core.utils import get_variant_combination


def create_single_variant(request, pk):
    """
    This view creates a single variant.
    It expects  variant name and variant options from a form.
    """
    product = models.Product.objects.get(pk=pk)

    if request.method == 'POST':
        variant_name = request.POST.get('variant_name', None)

        # TODO change form name to variant_options
        variant_options = request.POST.getlist('variant_option')

        sanitized_variant_options = [variant_option for variant_option in variant_options if variant_option != '']

        if variant_name is None:
            print("Error there is no variant_name")

        product_variant_metadata = models.ProductVariantMetadata.objects.create(variant_name=variant_name,
                                                                                options=sanitized_variant_options,
                                                                                product=product)

        product_variant_metadata.create_variants()

    return render(request, 'create_variant.html', {
        "product": product
    })


def create_multiple_variants(request, pk):
    product = models.Product.objects.get(pk=pk)

    if request.method == 'POST':
        request_body = request.POST
        variant_names = []

        for key in request_body.keys():
            if key != 'csrfmiddlewaretoken':
                variant_names.append(key)

        for name in variant_names:
            variant_options = request_body.getlist(name)

            sanitized_variant_options = [variant_option for variant_option in variant_options if variant_option != '']

            variant_metadata = models.ProductVariantMetadata.objects.create(product=product, variant_name=name,
                                                                            options=sanitized_variant_options)

            variant_metadata.create_variants()

        product.generate_variant_combinations()

    context = {'product': product}
    return render(request, "create-multiple-variants.html", context)


def generate_variant_combination(request, pk):
    # Get the product
    product = models.Product.objects.get(pk=pk)

    # Get the associated VariantMetadata
    color_variant_metadata = models.ProductVariantMetadata.objects.filter(product=product, variant_name="color").first()
    size_variant_metadata = models.ProductVariantMetadata.objects.filter(product=product, variant_name="size").first()
    material_variant_metadata = models.ProductVariantMetadata.objects.filter(product=product,
                                                                             variant_name="material").first()

    # Get a list of all Associated ColorVariants
    color_variants = models.ColorVariant.objects.filter(product_variant_metadata=color_variant_metadata)

    # Get a list of all Associated SizeVariants
    size_variants = models.SizeVariant.objects.filter(product_variant_metadata=size_variant_metadata)

    # Get a list of all Associated Material Variants
    material_variants = models.MaterialVariant.objects.filter(product_variant_metadata=material_variant_metadata)

    # Generate Combinations
    variant_combinations = get_variant_combination(color_variants, size_variants, material_variants)

    # Create Record
    for variant_combination in variant_combinations:
        color = variant_combination[0]
        size = variant_combination[1]
        material = variant_combination[2]

        models.ProductVariantCombination.objects.create(product=product, color_variant=color, size_variant=size,
                                                        material_variant=material)
    return redirect(reverse('product-details', args=[pk]))


class ProductListView(ListView):
    model = models.Product
    context_object_name = 'products'


class ProductDetailView(DetailView):
    model = models.Product

    # context_object_name = 'product_details'
    # product = get_object_or_404(models.Product)


class ProductCreateView(CreateView):
    model = models.Product
    fields = '__all__'

    def get_success_url(self):
        return reverse('product_list')


class ProductUpdateView(UpdateView):
    model = models.Product
    fields = '__all__'

    def get_success_url(self):
        return reverse('product_list')
    


class CombinationUpdateView(UpdateView):
    # product_id = models.Product.objects.get(pk=pk)
    model = models.ProductVariantCombination
    fields = ['price', 'sku']

    # def get_success_url(self, **kwargs):
    #     product_id = super().get_success_url(**kwargs)
    #     product_id['product_id'] = models.ProductVariantCombination.objects.filter(pk=self.get_object().pk)
        
    def get_success_url(self, **kwargs):
        return reverse("product-details", args=self.get_object().product_id)
    


# Get the product ID to add variant to
# Get the values of the variants entered
# Store the values in the db  -- Vague
# Take the different variants (from different tables) by ID associated to the product to make combination
# store each combination in table with an ID, price and SKU??


# def save_variant(request, pk):
#     product_variants = models.ProductVariantCombination.objects.get(pk=pk)

#     variant_combination = request.session.get('variant_combination')

#     if request.method == 'POST':
#         for variant in variant_combination  


def create_student(request):
    if request.method == 'POST':
        name = request.POST['name']
        age = request.POST['age']
        student = models.Student.objects.create(name=name, age=age)
        print(student.name, student.age)
    return render(request, "student.html")


# def updateproduct(request, pk):
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


#         updateproduct = models.Product.objects.get(pk=pk)
#         updateproduct.name = productname  # the item you have gotten .model field will be changed to what was given in th epost request
#         updateproduct.description = description
#         updateproduct.sku=sku
#         updateproduct.discount=discount
#         updateproduct.stock=stock
#         updateproduct.product_price=product_price
#         updateproduct.color=color
#         updateproduct.size=size
#         updateproduct.manufacturer=manufacturer
#         updateproduct.brand=brand
#         updateproduct.dimension=dimension
#         updateproduct.weight=weight
#         updateproduct.save()
#         return redirect(reverse("product", kwargs={"pk": updateproduct.category.pk}))
#     return render(request, "updateproduct.html")


def deleteproduct(request, pk):
    deleteproduct = models.Product.objects.get(pk=pk)
    deleteproduct.delete()
    return redirect(reverse("product_list"))


def delete_variant_combination(request, pk):
    variant_combination = models.ProductVariantCombination.objects.get(pk=pk)
    variant_combination.delete()
    product_id = variant_combination.product_id
    return redirect(reverse("product-details", args=[product_id]))


def delete_variant(request, pk):
    variant = models.ProductVariantMetadata.objects.get(pk=pk)
    variant.delete()
    product_id = variant.product_id
    return redirect(reverse("product-details", args=[product_id]))


def toggle_product_available(request, pk):
    product = models.Product.objects.get(pk=pk)
    product.is_available = not product.is_available
    product.save()
    return redirect(reverse("product", kwargs={"pk": product.category.pk}))
