from django.contrib.auth import get_user_model, login, logout
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie

from knox.auth import TokenAuthentication
from knox.models import AuthToken

from rest_framework import generics, permissions, status
from rest_framework.authentication import SessionAuthentication
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import (
    LoginSerializer,
    UserCreateSerializer,
    EditUserSerializer,
    ListUsersSerializer,
    CreateArticleSerializer,
    ListArticleSerializer,
    EditArticleSerializer,
    UserSerializer,
    ArticleDetailSerializer
)

User = get_user_model()

@ensure_csrf_cookie
def GetCsrfToken(request):
    return JsonResponse({'csrfToken': get_token(request)})

# ──────────────────────────────────────────────
# AUTH
# ──────────────────────────────────────────────

class Login(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        token = AuthToken.objects.create(user)[1]

        return Response({
            "user": {"username": user.username},
            "token": token
        }, status=status.HTTP_200_OK)

class LoginSession(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        login(request, user)

        return Response({
            "user": user.username,
        }, status=status.HTTP_200_OK)
    
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logged out successfully."}, status=status.HTTP_200_OK)
    
# ──────────────────────────────────────────────
# USERS
# ──────────────────────────────────────────────

class BaseUserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user
    
class UserDetailViewBackend(BaseUserDetailView):
    authentication_classes = [TokenAuthentication]

class UserDetailViewFrontend(BaseUserDetailView):
    authentication_classes = [SessionAuthentication]

class BaseUserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = ListUsersSerializer
    permission_classes = [permissions.IsAdminUser]

class UserListViewBackend(BaseUserListView):
    authentication_classes = [TokenAuthentication] 

class UserListViewFrontend(BaseUserListView):
    authentication_classes = [SessionAuthentication] 

class BaseUserCreateView(generics.CreateAPIView):
    serializer_class = UserCreateSerializer
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "User created successfully.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }, status=status.HTTP_201_CREATED)
    
class UserCreateViewBackend(BaseUserCreateView):
    authentication_classes = [TokenAuthentication]


class UserCreateViewFrontend(BaseUserCreateView):
    authentication_classes = [SessionAuthentication]

class BaseEditUserView(generics.RetrieveUpdateAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = EditUserSerializer

    def get_object(self):
        user_id = self.request.data.get('user_id')
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None

    def update(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response(
                {"error": "User not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        
        return Response({
            "id": instance.id,
            "username": instance.username,
            "email": instance.email,
            "first_name": instance.first_name,
            "last_name": instance.last_name
        })
    
class EditUserViewBackend(BaseEditUserView):
    authentication_classes = [TokenAuthentication]

class EditUserViewFrontend(BaseEditUserView):
    authentication_classes = [SessionAuthentication]

class BaseDeleteUserView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def delete(self, request):
        user_id = request.data.get('user_id')

        if not user_id:
            return Response(
                {"error": "'user_id' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user_to_delete = User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found."}, 
                status=status.HTTP_404_NOT_FOUND
            )

        user_to_delete.delete()
        return Response(
            {"message": "User deleted successfully."},
            status=status.HTTP_200_OK
        )
    
class DeleteUserViewBackend(BaseDeleteUserView):
    authentication_classes = [TokenAuthentication]

class DeleteUserViewFrontend(BaseDeleteUserView):
    authentication_classes = [SessionAuthentication]

# ──────────────────────────────────────────────
# ARTICLES
# ──────────────────────────────────────────────

class BaseArticleDetailView(generics.RetrieveAPIView):
    """Returns the details of a single article by slug."""
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    lookup_field = 'slug'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Article.objects.all()
        return Article.objects.filter(public="Public")

class ArticleDetailViewBackend(BaseArticleDetailView):
    authentication_classes = [TokenAuthentication]

class ArticleDetailViewFrontend(BaseArticleDetailView):
    authentication_classes = [SessionAuthentication]

class ListArticleView(generics.ListAPIView):
    serializer_class = ListArticleSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Article.objects.all()
        return Article.objects.filter(public="Public").order_by('-public_since')

class BaseCreateArticleView(generics.CreateAPIView):
    serializer_class = CreateArticleSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]
 
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class CreateArticleViewBackend(BaseCreateArticleView):
    authentication_classes = [TokenAuthentication]

class CreateArticleViewFrontend(BaseCreateArticleView):
    authentication_classes = [SessionAuthentication]

class BaseEditArticleView(generics.UpdateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = EditArticleSerializer
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        article_id = self.request.data.get('article_id')
        if not article_id:
            return None
        try:
            return Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return None

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()

        if not instance:
            return Response(
                {"error": "Article not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)
    
class EditArticleViewBackend(BaseEditArticleView):
    authentication_classes = [TokenAuthentication]

class EditArticleViewFrontend(BaseEditArticleView):
    authentication_classes = [SessionAuthentication]

class BaseDeleteArticleView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request):
        article_id = request.data.get('article_id')

        if not article_id:
            return Response(
                {"error": "'article_id' is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            article_to_delete = Article.objects.get(pk=article_id)
        except Article.DoesNotExist:
            return Response(
            {"error": "Article not found."},
            status=status.HTTP_404_NOT_FOUND
            )
        
        article_to_delete.delete()

        return Response(
            {"message": "Article deleted successfully."},
            status=status.HTTP_200_OK
        )
    
class DeleteArticleViewBackend(BaseDeleteArticleView):
    authentication_classes = [TokenAuthentication]

class DeleteArticleViewFrontend(BaseDeleteArticleView):
    authentication_classes = [SessionAuthentication]