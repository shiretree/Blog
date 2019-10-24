from django.contrib import admin

from blog.custom_site import custom_site     #不知道可不可行，待验证
from .models import Comment
# Register your models here.

@admin.register(Comment, site=custom_site)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('target','nickname','content','website','created_time')

