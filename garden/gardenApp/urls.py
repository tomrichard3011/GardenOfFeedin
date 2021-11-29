from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    path('', views.home, name='home'),
    path('signup', views.signup, name='signup'),
    path('createuser', views.createUser, name='createuser'),
    path('landing', views.landing, name='landing'),
    path('search', views.search, name='landing'),
    path('signin', views.signin, name='signin'),
    path('authenticate', views.authenticate, name='authenticate'),
    path('signout', views.signout, name='signout'),
    path('createpost', views.createPostPage, name='createpost'),
    path('createrequest', views.createRequestPage, name='createrequestpage'),
    path('makerequest', views.createRequest, name='createrequest'), 
    path('donation/donated/<int:id>', views.markAsDonated, name='mad'),
    path('managerequests', views.manageRequestPage, name='managerequestpage'),
    path('request/<int:id>', views.editRequestPage, name='requestpage'),
    path('request/edit/<int:id>', views.editRequest, name='editRequest'),
    path('request/delete/<int:id>', views.deleteRequest, name='deleteRequest'),
    # TEST URLS
    path('testmanagerequests', views.manageRequestPage, name='mrp'),
    path('testpostpage', views.createPostPage, name='cpp'),
    path('testpost', views.createPost, name='createpost'),
    path('profile', views.profile, name='testprofile'),
    path('changeProfileImage', views.changeProfileImage, name='cpi'),
    path('manage', views.manage, name='manage'),
    path('donation/<int:id>', views.donation, name='want'),
    path('donation/edit/<int:id>', views.editDonation, name='give'),
    path('donation/delete/<int:id>', views.deleteDonation, name='deletedonation'),
    path('messages', views.messages, name='messages'),
    path('createchat', views.createChat, name='createchat'),
    path('createmessage', views.createMessage, name='createmessage')

    # path('testhome', views.test_home, name='testhome'),
    # path('testlogin', views.test_login, name='testlogin'),
    # path('testcreate', views.test_createUser, name='testcreate'),
    # path('testmake', views.test_make, name='testmake'),
    # path('testvalidate',views.test_authenticate, name='testauthenticate')
] + \
    static(settings.STATIC_URL, document_root = settings.STATIC_ROOT) + \
    static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)