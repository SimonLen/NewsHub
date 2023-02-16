from django.contrib import admin
from .models import Author, Category, Post, PostCategory, Comment


def zero_rating(modeladmin, request, queryset):
    queryset.update(_rating=0)
    zero_rating.short_description = 'Обнулить рейтинг'


class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'type', 'creation_date', '_rating',)
    list_filter = ('author', 'type',)
    search_fields = ('title',)
    actions = [zero_rating]


admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post, PostAdmin)
admin.site.register(PostCategory)
admin.site.register(Comment)

# Register your models here.
