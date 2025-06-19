from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

#When the user visits the url on the website, the urlpatterns array is searched to find
#the url, if it is found a view from the path object is called with the requesr as the parameter

urlpatterns = [
    path("", views.home_view, name="home"),
    path("articles/", views.articles, name="articles"),
    path("article/<pk>/", views.article_detail, name="article_detail"),
    path("article_create/", views.article_create, name="article_create"),
    path("article_edit/<pk>/", views.article_edit, name="article_edit"),
    path("article_delete/<pk>/", views.article_delete, name="article_delete"),
    path("recipes/", views.recipes, name="recipes"),
    path("recipes_detail/<pk>/", views.recipe_detail, name="recipe_detail"),
    path("recipe_create/", views.recipe_create, name="recipe_create"),
    path("recipe_edit/<pk>/", views.recipe_edit, name="recipe_edit"),
    path("recipe_delete/<pk>/", views.recipe_delete, name="recipe_delete"),
    path("search/", views.search, name="search"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("account/", views.account_view, name="account"),
    path("settings/", views.settings_view, name="settings"),
    path("favourites/", views.favourites, name="favourites"),
    path("faq/", views.faq, name="faq"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
