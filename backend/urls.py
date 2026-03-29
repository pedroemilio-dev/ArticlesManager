from django.contrib import admin
from django.urls import path, re_path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView

from business.views import (
    # Auth
    Login,
    LoginSession,
    LogoutView,
    GetCsrfToken,

    # Users — Backend
    UserDetailViewBackend,
    UserCreateViewBackend,
    UserListViewBackend,
    EditUserViewBackend,
    DeleteUserViewBackend,

    # Users — Frontend
    UserDetailViewFrontend,
    UserCreateViewFrontend,
    UserListViewFrontend,
    EditUserViewFrontend,
    DeleteUserViewFrontend,

    # Articles
    ListArticleView,
    ArticleDetailViewBackend,
    ArticleDetailViewFrontend,
    CreateArticleViewBackend,
    DeleteArticleViewBackend,
    EditArticleViewBackend,
    CreateArticleViewFrontend,
    DeleteArticleViewFrontend,
    EditArticleViewFrontend,
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('knox.urls')),
    path('api/logout/', LogoutView.as_view(), name='logout'),

    # ── CSRF ────────────────────────────────────────────────────────
    path("api/csrf/", GetCsrfToken, name="get-csrf-token"),

    # ── Auth ─────────────────────────────────────────────────────────
    path('api/login/token/', Login.as_view(), name="login-token"),
    path('api/login/', LoginSession.as_view(), name="login-session"),

    # ── Users — Backend ───────────────────────────────────────────────
    path('api/backend/user/', UserDetailViewBackend.as_view(), name='user-detail'),
    path('api/backend/users/', UserListViewBackend.as_view(), name='user-list'),
    path('api/backend/users/create/', UserCreateViewBackend.as_view(), name='create-user'),
    path('api/backend/users/edit/', EditUserViewBackend.as_view(), name='edit-user'),
    path('api/backend/users/delete/', DeleteUserViewBackend.as_view(), name="delete-user"),

    # ── Articles — Backend ────────────────────────────────────────────
    path('api/backend/articles/', ListArticleView.as_view(), name="list-articles"),
    path('api/backend/articles/create/', CreateArticleViewBackend.as_view(), name="create-article"),
    path('api/backend/articles/edit/', EditArticleViewBackend.as_view(), name="edit-article"),
    path('api/backend/articles/delete/', DeleteArticleViewBackend.as_view(), name="delete-article"),
    path('api/backend/articles/<slug:slug>/', ArticleDetailViewBackend.as_view(), name='backend-article-detail'),
    
    # ── Users — Frontend ──────────────────────────────────────────────
    path('api/user/', UserDetailViewFrontend.as_view(), name='user-detail'),
    path('api/users/', UserListViewFrontend.as_view(), name='user-list'),
    path('api/users/create/', UserCreateViewFrontend.as_view(), name='create-user'),
    path('api/users/edit/', EditUserViewFrontend.as_view(), name='edit-user'),
    path('api/users/delete/', DeleteUserViewFrontend.as_view(), name="delete-user"),

    # ── Articles — Frontend ───────────────────────────────────────────
    path('api/articles/', ListArticleView.as_view(), name="list-articles"),
    path('api/articles/create/', CreateArticleViewFrontend.as_view(), name="create-article"),
    path('api/articles/edit/', EditArticleViewFrontend.as_view(), name="edit-article"),
    path('api/articles/delete/', DeleteArticleViewFrontend.as_view(), name="delete-article"),
    path('api/articles/<slug:slug>/', ArticleDetailViewFrontend.as_view(), name='frontend-article-detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


urlpatterns += [
    re_path(r'^(?!(api|admin|media|static)/).*$', TemplateView.as_view(template_name='index.html')),
]

