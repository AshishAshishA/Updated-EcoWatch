from django.urls import path
from .views import (showListOfAllBlogs, showListByCategory, createBlogs, 
            detailPostWithComments, updateBlogsView, deleteBlogsView, generate_gpt_input_value, customLoginView,
            Logout, customRegisterView, 
            )

urlpatterns=[
    path('',showListOfAllBlogs,name='home'),
    path('<int:id>/<slug:slug>',showListOfAllBlogs,name='home-updated'),
    path('category/<category>',showListByCategory, name='category'),
    path('my_post/<str:user>/<str:my_post>',showListOfAllBlogs, name='my-post'),

    path('create', createBlogs, name='create'),
    # path('create/<str:completion>', createBlogs, name='create-with-title'),

    path('detail/<slug:slug>/<int:id>', detailPostWithComments, name='detail'),

    path('update/<slug:slug>/<int:id>', updateBlogsView, name='update'),
    # path('update/<slug:slug>/<int:id>/<str:completion>', updateBlogsView, name='update-with-title'),

    path('delete/<int:pk>', deleteBlogsView, name='delete'),

    path("create/generate-with-gpt", generate_gpt_input_value, name="generate-with-gpt"),
    # path("update/generate-with-gpt/<slug:slug>/<int:id>", generate_gpt_input_value, name="generate-with-gpt-update"),

    path('login', customLoginView, name='login'),
    path('logout', Logout, name='logout'),
    path('register', customRegisterView, name='register'),

    # path('accounts/login/', AllAuthCustomLoginView.as_view(), name='account_login'),
    # path('accounts/signup/', AllAuthCustomSignupView.as_view(), name='account_signup'),
]