from django.urls import path
# from django.contrib.staticfiles.urls import staticfiles_urlpatterns
# from django.conf import settings
# from django.conf.urls.static import static
from . import views

urlpatterns = [
    path("import/", views.importExcel, name='push_excel'),
]
