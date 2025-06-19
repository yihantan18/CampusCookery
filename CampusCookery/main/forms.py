from django import forms
from .models import Recipe, Article, Tag, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .utils import resize_profile_picture

#This file is used to generate forms that inherit from django ModelForm class
#these forms are needed to make use of django validating techniques#

class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ("title", "ingredients", "body", "calorie_intake", "image", "time_taken")

class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ("title", "body", "image")

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("title",)

class UserSignupForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, help_text="Required.")
    email = forms.EmailField(max_length=254, help_text="Required. Enter a valid email address.")
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ("username", "first_name", "email", "password1", "password2", "profile_picture")

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.email = self.cleaned_data['email']
        if commit:
            user.save() # Save user, then create User Profile instance

            user_profile = UserProfile.objects.create(user=user)

            # Set profile picture
            if self.cleaned_data['profile_picture']:
                # Crop and resize to 256x256
                cropped_image = resize_profile_picture(self.cleaned_data['profile_picture'])
                user_profile.profile_picture.save(self.cleaned_data['profile_picture'].name, cropped_image, save=False)

            user_profile.save()

        return user

class UserUpdateForm(forms.ModelForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        # first_name field used for full name, due to django's handling
        # user not able to change username for security reasons
        fields = ("email", "first_name", "username", "profile_picture")

    def save(self, commit=True):
        user = super(UserUpdateForm, self).save(commit=False)
        if commit:
            user.save()
            # Ensure userprofile exists for user (should be redundant)
            if hasattr(user, 'userprofile'):
                user_profile = user.userprofile
            else:
                user_profile = UserProfile(user=user)

            # Set profile picture
            if self.cleaned_data['profile_picture']:
                # Crop and resize to 256x256
                cropped_image = resize_profile_picture(self.cleaned_data['profile_picture'])
                user_profile.profile_picture.save(self.cleaned_data['profile_picture'].name, cropped_image, save=False)
            user_profile.save()
        return user
