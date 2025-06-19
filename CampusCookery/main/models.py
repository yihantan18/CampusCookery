from django.db import models
from django.conf import settings
from django.contrib.auth.models import User

# Create your models here.
# Create tables by inheriting from the Model class
# Class = Table, object = record in the table, Attributes of the class = fields


class Recipe(models.Model):
    title = models.CharField(max_length=400)
    ingredients = models.TextField(max_length=20000)
    body = models.TextField(max_length=20000)
    calorie_intake = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="main/media/main", null=True)
    time_taken = models.CharField(max_length=100, null=True, blank=True)
    rating = models.IntegerField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.title


class Article(models.Model):
    title = models.CharField(max_length=400)
    body = models.TextField(max_length=20000)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="main/media/main", null=True)
    rating = models.IntegerField(max_length=3, null=True, blank=True)

    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=400)
    article = models.ManyToManyField(Article,null=True, blank=True)
    recipe = models.ManyToManyField(Recipe,null=True, blank=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

# Extended user to include profile picture
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to="profile_pictures/", null=True, blank=True)

    def __str__(self):
        return self.user.username


class Favourite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE, blank=True)

class UserRating(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, null=True, on_delete=models.CASCADE)
    article = models.ForeignKey(Article, null=True, on_delete=models.CASCADE, blank=True)
    rating = models.IntegerField(null=True)

class Faq(models.Model):
    question = models.CharField(max_length=2000)
    answer = models.CharField(max_length=2000)
