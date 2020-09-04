"""myBlog URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework import routers
from blog import views



post = routers.DefaultRouter()
post.register('PostAPI',views.Post_api)


user = routers.DefaultRouter()
user.register('UserAPI',views.User_api)

comment = routers.DefaultRouter()
comment.register('CommentsAPI',views.Comments_api)



urlpatterns = [
    #rabeeomran9944
    #0994480572

    path('admin/', admin.site.urls),
    path('', include('blog.urls')),

    #api

    path('post_api/', include(post.urls), name='1'),
    path('user_api/', include(user.urls), name='2'),
    path('comment_api/', include(comment.urls), name='2'),
]