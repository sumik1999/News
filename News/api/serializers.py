from News.models import Post
from rest_framework import serializers

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['title', 'content', 'date_posted' ,'author' ]
        read_only_fields =['date_posted','author']