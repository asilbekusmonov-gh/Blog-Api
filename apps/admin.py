from django.contrib import admin
from django.contrib.admin import ModelAdmin
from django.contrib.auth.admin import UserAdmin

from apps.models import Post, Like


class LikeInline(admin.StackedInline):
    model = Like
    extra = 0


@admin.register(Post)
class PostAdmin(ModelAdmin):
    inlines = [LikeInline]
    list_display = 'title', 'content', 'likes_count'
    readonly_fields = 'views_count',
    list_filter = ('category', 'is_published')
    search_fields = ('title', 'content')

    def likes_count(self, obj):
        return obj.likes.count()
