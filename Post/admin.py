from django.contrib import admin
from .models import Post
from .models import Reply
from .models import ReplyOfPost


# Register your models here.
admin.site.register(Post)
admin.site.register(Reply)
admin.site.register(ReplyOfPost)