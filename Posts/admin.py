from django.contrib import admin
from .models import Post, Comment, Followers,profile

# Register your models here.
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Followers)
admin.site.register(profile)
