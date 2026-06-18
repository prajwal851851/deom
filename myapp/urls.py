from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
from .views import book_list
from.views import  POSTSListCreateview, POSTSDetaliesView ,COMMENTSViewSet,COMMENTSDetaliesView,blogViewSet
from .views import ProtectedView, RegisterView, CustomTokenObtainPairView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import blogViewSet, ProtectedView


urlpatterns = [
    path('', views.home, name='home'),
    path('sinup/', views.sinup, name='sinup'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('contact/', views.contact, name='contact'),
    path('visit_youtube/', views.visit_youtube, name='visit_youtube'),
    path('visit_facebook/', views.visit_facebook, name='visit_facebook'),
    path('guest-visit/', views.guest_user, name='guest_user'),
    path('profile/', views.profile, name='profile'),  # Add trailing slash
    path('like/<int:post_id>/', views.like_post, name='like_post'),
    path('comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('edit/<int:post_id>/', views.edit_post, name='edit_post'),
    path('delete/<int:post_id>/', views.delete_post, name='delete_post'),
    path('follow/<int:user_id>/', views.follow_user, name='follow_user'),
    path('unfollow/<int:user_id>/', views.unfollow_user, name='unfollow_user'),
    path('book_list/', views.book_list, name='book_list'),
    # Posts
    path('POSTS/', POSTSListCreateview.as_view(), name='post-list-create'),
    path('POSTS/<int:pk>/', POSTSDetaliesView.as_view(), name='post-detail'),

    # Comments
    path('COMMENTS/', COMMENTSViewSet.as_view(), name='comment-list-create'),
    path('COMMENTS/<int:pk>/', COMMENTSDetaliesView.as_view(), name='comment-detail'),

    # Protected View
    path('api/protected/', ProtectedView.as_view(), name='protected-view'),
    path('api/login/', CustomTokenObtainPairView.as_view(), name='api-login'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/signup/', RegisterView.as_view(), name='api-signup'),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('blog/', blogViewSet.as_view({'get': 'list', 'post': 'create'}), name='blog-list'),
    path('protected-api-endpoint/', ProtectedView.as_view(), name='protected-api-endpoint'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)