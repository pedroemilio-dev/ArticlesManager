from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers

from .models import Article

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        request = self.context.get('request')

        user = authenticate(
            request=request,
            username=data.get('username'),
            password=data.get('password')
        )
        if not user or not user.is_active:
            raise serializers.ValidationError("Invalid credentials.")
        
        data['user'] = user 
        return data

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = fields

class ListUsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff']
        read_only_fields = fields
    
class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]  
    )

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name', 'is_staff']
        read_only_fields = ['id']
        extra_kwargs = {
            'email': {'required': True}, 
        }

    def create(self, validated_data):
        password = validated_data.pop('password')
        return User.objects.create_user(password=password, **validated_data)
    
class EditUserSerializer(serializers.ModelSerializer):
    user_id = serializers.UUIDField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ['user_id', 'username', 'email', 'first_name', 'last_name', 'password']
        extra_kwargs = {
            'username': {'read_only': True},
            'email': {'required': False},
            'first_name': {'required': False},
            'last_name': {'required': False},
            'password': {'write_only': True, 'required': False, 'validators': [validate_password]},
        }

    def validate_user_id(self, value):
        if not User.objects.filter(pk=value).exists():
            raise serializers.ValidationError("User not found.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop('user_id', None)

        password = validated_data.pop('password', None)
        if password:
            instance.set_password(password)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()
        return instance

# ──────────────────────────────────────────────
# ARTICLE SERIALIZERS
# ──────────────────────────────────────────────

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']

class ArticleDetailSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    mainImage = serializers.ImageField(use_url=True)

    class Meta:
        model = Article
        fields = ['id', 'title', 'description', 'tags', 'createdAt', 'public',
                  'author', 'mainImage', 'public_since', 'slug']
        read_only_fields = fields

class ListArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer(read_only=True)
    mainImage = serializers.ImageField(use_url=True)

    class Meta:
        model = Article
        fields = ["id", "title", "description", "tags", "createdAt", "public", "author", "mainImage", "public_since", "slug"]
        read_only_fields = fields

class CreateArticleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Article
        fields = ["id", "title", "description", "tags", "createdAt", "public", "author", "mainImage"]
        extra_kwargs = {"author": {"read_only": True}}

class EditArticleSerializer(serializers.ModelSerializer):
    article_id = serializers.IntegerField(write_only=True)
    public_since = serializers.DateTimeField(required=False, allow_null=True)

    class Meta:
        model = Article
        
        fields = ['article_id', 'title', 'description', 'tags', 'public', 'mainImage', 'public_since']
        extra_kwargs = {
            'title': {'required': False},
            'description': {'required': False},
            'tags': {'required': False},
            'public': {'required': False},
            'mainImage': {'required': False},
            'public_since': {'required': False},    
        }

    def validate_article_id(self, value):
        if not Article.objects.filter(pk=value).exists():
            raise serializers.ValidationError("Article not found.")
        return value

    def update(self, instance, validated_data):
        validated_data.pop('article_id', None)
        return super().update(instance, validated_data)