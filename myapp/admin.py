from django.contrib import admin
from myapp.models import feature, next
from.models import Contact_Message
from .models import user_activity
from .models import Post
from .models import Like,Comment,UserProfile,Follow,my_Customer,my_Order,Book,POSTS,COMMENTS


@admin.register(Contact_Message)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'message', 'created_at')
    
    


@admin.register(user_activity)
class UserActivityAdmin(admin.ModelAdmin):
    list_display = ('user', 'activity', 'visited_at')
    list_filter = ('activity', 'visited_at')
    search_fields = ('user__username', 'activity')
    ordering = ('-visited_at',)  # Sort by 'visited_at' descending
    date_hierarchy = 'visited_at'




admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Like)
admin.site.register(Comment) 
admin.site.register(Follow)
admin.site.register(my_Customer)
admin.site.register(my_Order)
admin.site.register(Book)    
admin.site.register(POSTS)
admin.site.register(COMMENTS)
