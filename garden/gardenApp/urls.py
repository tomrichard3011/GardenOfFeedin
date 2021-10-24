from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.test_home, name='home'),
    path('login', views.test_login, name='test'),
    path('create', views.test_createUser, name='create'),
    path('make', views.test_make, name='make'),
    path('validate',views.test_authenticate, name='authenticate')
] + static(settings.STATIC_URL,
document_root = settings.STATIC_ROOT)