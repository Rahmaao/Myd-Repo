from django.urls import path
from core.views import *

urlpatterns = [
    path("categorieslist/", category_views.CategoryListView.as_view(), name="category-list"), #category_list.html
    path("categorieslist/<int:pk>", category_views.CategoryDetailView.as_view(), name="category-detail"), #category_detail.html
    path("category/add/", category_views.CategoryCreateView.as_view(), name="category-add"), #category_form.html
    path('category_update/<int:pk>/', category_views.CategoryUpdateView.as_view(), name='category-update'), #category_form.html
    path("categories_delete/<int:pk>", category_views.delete_category, name="delete-category"),
    path("products/add/", product_views.ProductCreateView.as_view(), name="product-add"), #product_form.html
    path("products_list", product_views.ProductListView.as_view(), name="product_list"), #product_list.html
    path('product_update/<int:pk>/', product_views.ProductUpdateView.as_view(), name='product-update'), #product_form.html
    path("products/<int:pk>", product_views.ProductDetailView.as_view(), name="product-details"), #product_detail.html
#     path("products/<int:pk>/create-single-variant/", product_views.create_single_variant, name="create-single-variant"),
    path("products/<int:pk>/create-multiple-variants", product_views.create_multiple_variants,
         name="create-multiple-variants"), #create_multiple_variants.html
    path("products/<int:pk>/generate-variant-combination/", product_views.generate_variant_combination,
         name='generate-variant-combination'),
    # path("updateproduct/<int:pk>", product_views.updateproduct, name="updateproduct"),
    path("deleteproduct/<int:pk>", product_views.deleteproduct, name="delete-product"),
    path("deletecombination/<int:pk>", product_views.delete_variant_combination, name="delete-combination"),
#     path("deletevariant/<int:pk>", product_views.delete_variant, name="delete-variant"),
    path("combination_update/<int:pk>/", product_views.CombinationUpdateView.as_view(), name='combination-update'),
#     path("isavailable/<int:pk>", product_views.toggle_product_available, name="available"),
    # path("test/", product_views.create_product_variants, name="test-product"),
#     path("addvariant/<int:pk>", product_views.create_single_variant, name='create-variant'),
#     path("import/", common_views.importExcel, name="push-excel"),
#     path("createstudent/", product_views.create_student, name="student"),
]
