from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('createuser', views.createUser, name='createuser'),
    path('landing', views.landing, name='landing'),
    path('signin', views.signin, name='signin'),
    path('authenticate', views.authenticate, name='authenticate'),
    path('signout', views.signout, name='signout'),

    # TEST URLS
    path('testpostpage', views.createPostPage, name='cpp'),
    path('testpost', views.createPost, name='createpost'),
    # path('testhome', views.test_home, name='testhome'),
    # path('testlogin', views.test_login, name='testlogin'),
    # path('testcreate', views.test_createUser, name='testcreate'),
    # path('testmake', views.test_make, name='testmake'),
    # path('testvalidate',views.test_authenticate, name='testauthenticate')
] + \
    static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)