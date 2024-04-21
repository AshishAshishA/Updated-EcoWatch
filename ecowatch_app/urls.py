from django.urls import path
from . import views

urlpatterns = [
    path('', views.waste_site_list, name='waste_site_list'),
    path('my_post/<str:my_post>',views.waste_site_list, name='my-post'),
    # path('<city>',views.waste_site_list_by_city, name='waste_site_list_by_city'),
    path('upload-and-tag/',views.upload_and_tag, name='upload_and_tag'),

    path('login', views.CustomLoginView.as_view(), name='eco-login'),
    path('logout', views.Logout, name='eco-logout'),
    path('register', views.CustomRegisterView.as_view(), name='eco-register'),

    # path('accounts/login/', views.AllAuthCustomLoginView.as_view(), name='eco_account_login'),
    # path('accounts/signup/', views.AllAuthCustomSignupView.as_view(), name='eco_account_signup'),
]
