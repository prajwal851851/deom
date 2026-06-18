from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils import timezone


class feature(models.Model):  
    
    name=models.CharField(max_length=50)
    email=models.EmailField
    phone=models.CharField(max_length=10)
    message=models.CharField(max_length=5000)
def __str__(self):
    return self.name
        
        
class next(models.Model):
    user=models.CharField(max_length=50)
    summery=models.CharField(max_length=5000)
    
def __str__(self):
    return self.user

class Contact_Message(models.Model):  
    
    name=models.CharField(max_length=50)
    phone=models.CharField(max_length=10)
    message=models.CharField(max_length=5000)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
def __str__(self):
    return f"message from {self.name}({self.email})"


class user_activity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity = models.CharField(max_length=5000)
    visited_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username} visited {self.activity} at {self.visited_at}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pictures/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='post_images/', blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Post by {self.user.username}"

    def like_count(self):
        return self.like_set.count()

    def has_user_liked(self, user):
        return self.like_set.filter(user=user).exists()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = ('user', 'post')

    def __str__(self):
        return f"Like by {self.user.username} on {self.post}"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.username} on {self.post}"
    
    
class Follow(models.Model):
    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # Prevent duplicate follows

    def __str__(self):
        return f"{self.follower.username} follows {self.followed.username}"    
    
class my_Customer(models.Model):
    customer_id = models.IntegerField()
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    age = models.IntegerField()
    
    
    class Meta:
        db_table = 'my_Customer'
        
    
class my_Order(models.Model):
    order_id = models.IntegerField()
    customer_id = models.IntegerField()
    product=models.CharField(max_length=100)
    quantity=models.IntegerField()
    price=models.IntegerField()
    
    class Meta:
        db_table = 'my_Order'
    
    
class Book(models.Model):
    book_id = models.AutoField(primary_key=True, serialize=False)
    name = models.CharField(max_length=100)
    author = models.CharField(max_length=100)
    price = models.IntegerField()
    publiced_date = models.DateField()
    
    class Meta:
        db_table = 'book'
        
    def __str__(self):
        return f"{self.name} by {self.author}"
    
    
    
class POSTS(models.Model):
    post_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    

    
class blog(models.Model):
    post_id = models.AutoField(primary_key=True)
    title=models.CharField(max_length=100)
    content=models.CharField(max_length=1000)
    author=models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
    
class COMMENTS(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post=models.ForeignKey(blog, related_name='comment',on_delete=models.CASCADE)    
    name=models.CharField(max_length=100)
    body=models.CharField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f'comment by {self.name} on {self.post} posts'
        