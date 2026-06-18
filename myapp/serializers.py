from django.contrib.auth.models import User,Group
from rest_framework import routers, serializers, viewsets, permissions
from .models import Book,POSTS,COMMENTS,blog

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
        
class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'
        
class permissionsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = permissions
        fields = '__all__'
        

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'    
        
class POSTSSerializer(serializers.ModelSerializer):   
    
    class Meta:
        model=POSTS
        fields = '__all__'
        
class COMMENTSserializers(serializers.ModelSerializer):
    class Meta:
        model=COMMENTS
        fields = '__all__'
 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'password']
        extra_kwargs = {'password': {'write_only': True}}
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user    
        


class blogSerializer(serializers.HyperlinkedModelSerializer):
    COMMENTS=serializers.HyperlinkedRelatedField(many=True,view_name='comment-detail',read_only=True)
    class Meta:
        model = blog
        fields = '__all__'