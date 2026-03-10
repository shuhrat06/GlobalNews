from django.contrib import admin
from .models import *

class ContentInline(admin.StackedInline):
    model = Content

@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = (ContentInline,)

admin.site.register(
    [
        Category,
        Contact,
        Newsletter,
        Tag,
        Comment,
        Content,
        Moment
    ]
)