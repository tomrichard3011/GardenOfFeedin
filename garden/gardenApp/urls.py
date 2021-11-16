from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('createuser', views.createUser, name='createuser'),
    # TEST URLS
    path('testhome', views.test_home, name='testhome'),
    path('testlogin', views.test_login, name='testlogin'),
    path('testcreate', views.test_createUser, name='testcreate'),
    path('testmake', views.test_make, name='testmake'),
    path('testvalidate',views.test_authenticate, name='testauthenticate')
] + static(settings.STATIC_URL,
document_root = settings.STATIC_ROOT)