from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name='index'),
    path("users/", views.users, name='users'),
    path("import/", views.importExcel, name='push_excel'),
]
