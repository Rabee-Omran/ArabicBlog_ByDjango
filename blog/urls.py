from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from django.conf.urls.static import static
from django.conf import settings

from blog import views
from django.conf.urls import include
from rest_framework import routers
from blog.views import delete_own_comment


urlpatterns = [
   
    path('', views.home,name = "home"),
    path('about/', views.about, name="about"),
   
    path('detail/<int:post_id>/', views.post_detail, name="detail"),
    path('<int:comment_id>*<int:post_id>*', delete_own_comment, name='delete_comment'),
    path('new_post/', views.PostCreateView.as_view(), name='new_post'),
    path('detail/<slug:pk>/update/', views.PostUpdateView.as_view(), name="post_update"),
    path('detail/<slug:pk>/delete/', views.PostDeleteView.as_view(), name="post_delete"),
    
    path('register/', views.register, name="register"),
    # path('login/', LoginView.as_view(template_name='login.html'), name="login"),
    # path('logout/', LogoutView.as_view(template_name='logout.html'), name="logout"),
    path('login/', views.login_user, name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/', views.profile, name="profile"),
    path('profile_update/', views.profile_update, name="profile_update"),


    

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
