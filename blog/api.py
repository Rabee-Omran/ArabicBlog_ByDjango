from .models import Post, Comment
from rest_framework import serializers
from django.contrib.auth.models import User

class PostAPI(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields ='__all__'



class UserAPI(serializers.ModelSerializer):
    class Meta:
        model = User
        fields ='__all__'


class CommentsAPI(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields ='__all__'







