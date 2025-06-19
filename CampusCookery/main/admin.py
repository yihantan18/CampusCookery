from django.contrib import admin
from .models import Recipe, Article, Tag, UserProfile, Favourite, UserRating

# Register your models here.
admin.site.register(Recipe)
admin.site.register(Article)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Favourite)
admin.site.register(UserRating)