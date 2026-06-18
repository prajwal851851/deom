import re
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from django.http import HttpResponse
from .models import feature, next
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate,login
from django.contrib.auth.hashers import make_password, check_password
from django.core.mail import send_mail
from django.conf import settings
import random
from django.db import models
from .models import Contact_Message
from django.contrib.auth.decorators import login_required
from .models import user_activity
from.models import Post
from.forms import PostForm
from django.shortcuts import  get_object_or_404
from django.http import JsonResponse
from .models import Like,Comment
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django import template
from .forms import UserProfileForm, PostForm, CommentForm
from .models import UserProfile, Post, Like, Comment
from .models import Follow, User
from django.contrib.auth.models import Group, User, Permission
from rest_framework import permissions, viewsets
from .models import Book,POSTS,COMMENTS
from myapp.serializers import GroupSerializer, UserSerializer,permissionsSerializer,BookSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import COMMENTSserializers,POSTSSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework import status
from .serializers import UserSerializer,POSTSSerializer
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from .models import blog
from .serializers import blogSerializer
from .filter import blogFilter
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.permissions import AllowAny
from .pagination import blogcursorPagination
from rest_framework.throttling import SimpleRateThrottle
from rest_framework_simplejwt.views import TokenObtainPairView

# Temporary OTP storage
otp_storage = {}


# Custom Throttle Classes for Signup and Signin
class SignupThrottle(SimpleRateThrottle):
    """
    Throttle for signup endpoint: 5 attempts per day per IP address
    """
    scope = 'signup'
    
    def get_cache_key(self):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(self.request)
        }


class SigninThrottle(SimpleRateThrottle):
    """
    Throttle for signin endpoint: 10 attempts per hour per IP address
    """
    scope = 'signin'
    
    def get_cache_key(self):
        return self.cache_format % {
            'scope': self.scope,
            'ident': self.get_ident(self.request)
        }


def home(request):
    features = feature.objects.all()
    nexts = next.objects.all()
    return render(request, "index.html", {"features": features, "nexts": nexts})


def sinup(request):
    if request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        
        # Check if passwords match
        if password != confirm_password:
            messages.info(request, 'Passwords do not match')
            return render(request,'sinup.html',{"name":name, "email":email})
        
        # Validate password complexity
        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', password):
            messages.info(request, 'Password must contain at least one uppercase letter, one number, one special character, and be at least 8 characters long.')
            return render(request,'sinup.html',{"name":name, "email":email})
        
        # Check if email or username already exists
        if User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return render(request,'sinup.html',{ "name":name})
        
        elif User.objects.filter(username=name).exists():
            messages.info(request, 'Username already exists')
            return render(request,'sinup.html',{"email":email})
        
        # Create the user
        else:
         user = User.objects.create_user(username=name, email=email, password=password)
         user.save()
         messages.success(request, 'Account created successfully! Please log in.')
         return redirect('login')
    
    else:
        return render(request, "sinup.html")


def login(request):
    if request.method == "POST":
        name = request.POST['username']
        password = request.POST['password']
        
         #authenticate the user
        user = auth.authenticate(request, username=name, password=password)
        
        if user is not None:
            auth.login(request,user)
            messages.info(request,"you have login successfully")
            return redirect("home")
        else:
            messages.info(request,"invalid username or password")
            return redirect('login')
    else:
        return render(request,'login.html')
    
def logout(request):
    auth.logout(request)
    messages.success(request,"you have logout successfully")
    return render(request,'login.html')

def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']
        try:
            user = User.objects.filter(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email does not exist")
            return redirect('forgot_password')

        otp = random.randint(10000, 99999,)
        otp_storage[email] = otp

        send_mail(
            subject='Password Reset OTP',
            message=f'Your OTP is: {otp} DO NOT SHARE WITH ANYONE',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[email],
        )
        messages.success(request, "OTP sent to your email")
        request.session['reset_email'] = email
        return redirect("verify_otp")
    return render(request, "forgot_password.html")


def verify_otp(request):
    if request.method == "POST":
        otp = request.POST['otp']
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect("forgot_password")

        if otp_storage.get(email) == int(otp):
            otp_storage.pop(email, None)
            messages.success(request, "OTP verified. Reset your password.")
            return redirect("reset_password")
        else:
            messages.error(request, "Invalid OTP")
            return redirect("verify_otp")
    return render(request, "verify_otp.html")


def reset_password(request):
    if request.method == "POST":
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']
        email = request.session.get('reset_email')

        if not email:
            messages.error(request, "Session expired. Please try again.")
            return redirect("forgot_password")

        if new_password != confirm_password:
            messages.error(request, "Passwords do not match")
            return render(request,"reset_password.html",{'error_message':'password does not match'})

        if not re.match(r'^(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$', new_password):
            messages.error(request,"Password must contain at least one uppercase letter, one number, one special character, and be at least 8 characters long.")
            return redirect("reset_password")

        
        user = User.objects.filter(email=email).first()
        if user is None:
            messages.error(request, "User does not exist")
            return redirect("reset_password")

        if check_password(new_password, user.password):
            messages.error(request, "New password cannot be the same as the old password")
            return render(request,"reset_password",{'error_message':'old password must not be new password try another password'})

        user.password = make_password(new_password)
        user.save()
        messages.success(request, "Password reset successfully. Please log in.")
        return redirect("login")
    return render(request, "reset_password.html")

@login_required
def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

       
        try:
            # Save the message to the database
            contact_message = Contact_Message(  
                name=name,
                phone=phone,
                message=message,
            )
            contact_message.save()

            # Send email notification
            subject = f"Message from {name} ({email})"
            body = f"Name: {name}\nEmail: {email}\nPhone: {phone}\nMessage: {message}"
            send_mail(
                subject,
                body,
                settings.DEFAULT_FROM_EMAIL,
                [settings.DEFAULT_FROM_EMAIL],
                fail_silently=False,
            )

            return redirect("home")

        except UserWarning as e:
            return render(request, "contact.html", {'error_message': f"An error occurred: {str(e)}"})

    return render(request, "contact.html")




@login_required
def visit_youtube(request):
    user_activity.objects.create(user=request.user, activity='youtube')
    return redirect("https://www.youtube.com/watch?v=rfscVS0vtbw")


@login_required
def visit_facebook(request):
    user_activity.objects.create(user=request.user, activity='facebook')
    return redirect("https://www.facebook.com/prajwal.dhital.7547/")


def guest_user(request):
    return render(request, 'home')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    posts = Post.objects.filter(user=request.user).order_by('-created_at')

    if request.method == 'POST':
        if 'update_profile' in request.POST:
            profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
            if profile_form.is_valid():
                profile_form.save()
                return redirect('profile')
        elif 'create_post' in request.POST:
            post_form = PostForm(request.POST, request.FILES)
            if post_form.is_valid():
                post = post_form.save(commit=False)
                post.user = request.user
                post.save()
                return redirect('profile')
    else:
        profile_form = UserProfileForm(instance=user_profile)
        post_form = PostForm()

    return render(request, 'profile.html', {
        'profile': user_profile,
        'posts': posts,
        'profile_form': profile_form,
        'post_form': post_form,
    })

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return JsonResponse({'like_count': post.like_count(), 'liked': created})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            comment = Comment.objects.create(user=request.user, post=post, content=content)
            return JsonResponse({
                'username': comment.user.username,
                'content': comment.content,
                'created_at': comment.created_at.strftime("%b %d, %Y %I:%M %p")
            })
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    if request.method == 'POST':
        content = request.POST.get('content')
        post.content = content
        post.save()
        return JsonResponse({'content': post.content})
    return JsonResponse({'error': 'Invalid request'}, status=400)

@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, user=request.user)
    post.delete()
    return JsonResponse({'success': True})





@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)  # Get the user to follow
    follow, created = Follow.objects.get_or_create(
        follower=request.user,  # Current user is the follower
        followed=user_to_follow  # User to follow
    )
    if not created:
        follow.delete()  # If the follow relationship already exists, delete it (unfollow)
    return JsonResponse({'followed': created})  # Return whether the user is now followed

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return JsonResponse({'status': 'success', 'followed': False})




class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all().order_by('name')
    serializer_class = GroupSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    
class permissionViewset(viewsets.ModelViewSet):
    queryset = Permission.objects.all().order_by('name')
    serializer_class = permissionsSerializer
    permission_classes = [permissions.IsAuthenticated]
    
@api_view(['GET'])
def book_list(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)

class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    
    
    
class POSTSListCreateview(ListCreateAPIView):
     """
    GET: List all posts
    POST: Create a new post
    """
     queryset = POSTS.objects.all()
     serializer_class = POSTSSerializer
class POSTSDetaliesView(RetrieveUpdateDestroyAPIView):
    """
    GET: Retrieve a single post
    PUT: Update a post
    PATCH: Partially update a post
    DELETE: Delete a post
    """
    queryset = POSTS.objects.all()
    serializer_class = POSTSSerializer
    
    


class COMMENTSViewSet(ListCreateAPIView):
    queryset = COMMENTS.objects.all()
    serializer_class = COMMENTSserializers
    

class COMMENTSDetaliesView(RetrieveUpdateDestroyAPIView):
    queryset = COMMENTS.objects.all()
    serializer_class = COMMENTSserializers
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({"message": "You have access."})
    
        
        

    
    
class RegisterView(APIView):
    throttle_classes = [SignupThrottle]
    
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
     
"""" curl -X GET http://127.0.0.1:8000/api/protected/ -H "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQwNDcyMzQ3LCJpYXQiOjE3NDA0NzE2ODgsImp0aSI6ImY5ZGMxYTY4OGJiYjQ4OGJhN2NjZjZkYTMwMWVhOGFlIiwidXNlcl9pZCI6OH0.0ul1rfVjjfU8-Fu_clNYzkfpqqFLZxNBUAZJd7Ln0gQ"
"""


class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Custom Login View with throttling
    Throttle: 10 attempts per hour per IP address
    """
    throttle_classes = [SigninThrottle]


        
    
        
        
        
class blogViewSet(viewsets.ModelViewSet):
    queryset = blog.objects.all()
    serializer_class = blogSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = blogFilter
    search_fields = ['title']
    ordering_fields = ['created_at', 'title']
    ordering=['-created_at']
    permission_classes = [AllowAny] 
    pagination_class = blogcursorPagination
    
    
class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response({"message": "You are authenticated!"})    
                