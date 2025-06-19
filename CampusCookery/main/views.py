from pip._internal import req
from django.db.transaction import commit
from django.shortcuts import render, redirect
from .models import Recipe, Article, Tag, UserProfile, Favourite, UserRating, Faq
from .forms import RecipeForm, ArticleForm, TagForm, UserUpdateForm, UserSignupForm
from django.contrib.auth import login,logout, authenticate, get_user_model




#The function that renders the homepage
def home_view(request):
    context = {
        "recipes": Recipe.objects.all(),
    }
    return render(request, "main/home.html", context)

#The function that renders the signup page if the user sends a get request
#if the user sends a post request, the data is validated and if it is valid,
#a new user is created
def signup_view(request):
    if request.POST:
        form = UserSignupForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
    else:
        form = UserSignupForm()

    context = {
        "form": form,
    }

    return render(request, "main/signup.html", context)

#The function that renders the login page if the user sends a get request
#if the user sends a post request, the data is validated and if it is valid,
#the user is logged in
def login_view(request):
    if request.POST:
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")
        else:
            error_message = "Invalid username or password"

            return render(request, "main/login.html", {"error_message": error_message})

    return render(request, "main/login.html")

#The function that logs the user out
def logout_view(request):
    logout(request)
    return redirect("/")

#The function that renders the page with user account page if they are logged in
def account_view(request):
    if not request.user.is_authenticated:
        return redirect("login")
    try:
        user_profile = UserProfile.objects.get(user=request.user)
        recipes = Recipe.objects.filter(author=request.user)
        articles = Article.objects.filter(author=request.user)

        context = {
            'user_profile': user_profile,
            'recipes': recipes,
            'articles': articles
        }
    except:
        context = {}

    return render(request, "main/account.html", context)

#The function that renders the page with the user account edit form if the request type is GET
#If request type is POST, it validates the data and updates the user account details
def settings_view(request):
    """Enables user to edit account, and change theme"""
    if not request.user.is_authenticated:
        return redirect("login")

    if request.POST:
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)

        if form.is_valid():
            form.save()
            return redirect("account")
    else:
        form = UserUpdateForm(instance=request.user)

    user_profile = UserProfile.objects.get(user=request.user)

    context = {
        'form': form,
        'user_profile': user_profile,
    }

    return render(request, "main/settings.html", context)

#The function that renders the page with all the articles from the db
def articles(request):
    articles = Article.objects.all()
    context = {"articles": articles}

    return render(request, "main/articles.html", context)

#The function that renders the page with the details of the certain article
def article_detail(request, pk):
    article = Article.objects.get(id=pk)
    if request.method == "POST" and request.user.is_authenticated:
        if request.POST.get("rating") is not None:
            try:
                ur = UserRating.objects.get(user=request.user, article=article)
                ur.delete()
            except:
                pass
            ur = UserRating.objects.create(user=request.user, article=article, rating=request.POST.get("rating"))
            ur.save()

        if request.POST.get("fav") == "true":
            # Ensure favourite cannot be added multiple times
            if not Favourite.objects.filter(user=request.user, article=article).exists():
                fav = Favourite.objects.create(user=request.user, article=article)
                fav.save()
        else:
            fav = Favourite.objects.filter(user=request.user, article=article).first()
            if fav:
                fav.delete()

    rating_sum = 0
    rating_cnt = 0
    rating = None
    for r in UserRating.objects.filter(article=article):
        if r.rating is not None:
            rating_sum += int(r.rating)
            rating_cnt += 1
    if rating_cnt != 0:
        rating = rating_sum / rating_cnt
    try:
        favourite = Favourite.objects.get(user=request.user, article=article)
    except:
        favourite = None
    context = {
        "article": article,
        "rating": rating,
        "favourite": favourite,
    }
    return render(request, "main/article.html", context)

#The function that renders the page with article create form if the request type is get
#If the request type is post, it validates the data and creates a new article in the db
def article_create(request):
    if not request.user.is_authenticated:
        return redirect("login")
    if request.POST:
        form = ArticleForm(request.POST, request.FILES)
        print(request.POST)
        if form.is_valid():
            new_article = form.save(commit=False)
            new_article.author = request.user
            new_article.save()
            tags = request.POST.getlist("tags")
            for tag in tags:
                t = Tag.objects.get(title=tag)
                t.article.add(new_article)
            return redirect("/")
    else:
        form = ArticleForm()

    context = {
        "form": ArticleForm,
        "tags": Tag.objects.all(),
    }

    return render(request, "main/article_create.html", context)

#The function that renders the page with article edit form if the request type is get
#If the request type is post, it validates the data and edits the article in the db
def article_edit(request, pk):
    edited_article = Article.objects.get(id=pk)

    if not request.user.is_authenticated or not request.user == edited_article.author:
        return redirect("login")

    if request.POST:
        form = ArticleForm(request.POST, request.FILES, instance=edited_article)

        if form.is_valid():
            form.save()

            tags = request.POST.getlist("tags")
            try:
                for tag in Tag.objects.get(article=edited_article):
                    tag.article.remove(edited_article.id)
            except:
                pass
            for tag in tags:
                t = Tag.objects.get(title=tag)
                t.article.add(edited_article.id)
            return redirect("/")
    else:
        form = ArticleForm(instance=edited_article)

    context = {
        "pk": pk,
        "form": form,
    }
    return render(request, "main/article_edit.html", context)

#The function to delete an article from the db
def article_delete(request, pk):
    if request.user.is_authenticated:
        article_to_delete = Article.objects.get(id=pk)
        if request.user == article_to_delete.author:
            if request.POST:
                article_to_delete.delete()
        else:
            return redirect("login")
    else:
        return redirect("login")

#The function that renders the page with all the recipes from the db
def recipes(request):
    tags = Tag.objects.prefetch_related("recipe")

    context = {tags: tags}

    return render(request, "main/recipes.html", context)

#The function that renders the page with the details of the certain recipe
def recipe_detail(request, pk):
    recipe = Recipe.objects.get(id=pk)
    if request.method == "POST" and request.user.is_authenticated:
        if request.POST.get("rating") is not None:
            try:
                ur = UserRating.objects.get(user=request.user, recipe=recipe)
                ur.delete()
            except:
                pass
            ur = UserRating.objects.create(user=request.user, recipe=recipe, rating=request.POST.get("rating"))
            ur.save()

        if request.POST.get("fav") == "true":
            # Ensure favourite cannot be added multiple times
            if not Favourite.objects.filter(user=request.user, recipe=recipe).exists():
                fav = Favourite.objects.create(user=request.user, recipe=recipe)
                fav.save()
        else:
            fav = Favourite.objects.filter(user=request.user, recipe=recipe).first()
            if fav:
                fav.delete()

    rating_sum = 0
    rating_cnt = 0
    rating = None
    for r in UserRating.objects.filter(recipe=recipe):
        if r.rating is not None:
            rating_sum += int(r.rating)
            rating_cnt += 1
    if rating_cnt != 0:
        rating = rating_sum / rating_cnt
    try:
        favourite = Favourite.objects.get(user=request.user, recipe=recipe)
    except:
        favourite = None
    context = {
        "recipe": recipe,
        "rating": rating,
        "favourite": favourite,
    }
    return render(request,"main/recipe.html", context)

#The function that renders the page with recipe create form if the request type is get
#If the request type is post, it validates the data and creates a new recipe in the db
def recipe_create(request):
    if not request.user.is_authenticated:
        return redirect("login")

    if request.POST:
        form = RecipeForm(request.POST, request.FILES)
        if form.is_valid():
            new_recipe = form.save(commit=False)
            new_recipe.author = request.user
            new_recipe.save()
            tags = request.POST.getlist("tags")
            for tag in tags:
                t = Tag.objects.get(title=tag)
                t.recipe.add(new_recipe.id)
                print(t.recipe)
            return redirect("/")
    else:
        context = {
            "form": RecipeForm,
            "tags": Tag.objects.all(),
        }
        return render(request, "main/recipe_create.html", context)

#The function that renders the page with recipe edit form if the request type is get
#If the request type is post, it validates the data and edits the recipe in the db
def recipe_edit(request, pk):
    edited_recipe = Recipe.objects.get(id=pk)

    if not request.user.is_authenticated or not request.user == edited_recipe.author:
        return redirect("login")

    if request.POST:
        form = RecipeForm(request.POST, request.FILES, instance=edited_recipe)
        if form.is_valid():
            form.save()
            try:
                for tag in Tag.objects.get(recipe=edited_recipe):
                    tag.recipe.remove(edited_recipe.id)
            except:
                pass
            tags = request.POST.getlist("tags")
            for tag in tags:
                t = Tag.objects.get(title=tag)
                t.recipe.add(edited_recipe.id)
            return redirect("/")
    else:
        form = RecipeForm(instance=edited_recipe)

    context = {
        "pk": pk,
        "form": form,
    }

    return render(request, "main/recipe_edit.html", context)

#The function to delete an article from the db
def recipe_delete(request, pk):
    if request.user.is_authenticated:
        recipe_to_delete = Recipe.objects.get(id=pk)
        if request.user == recipe_to_delete.author:
            if request.POST:
                recipe_to_delete.delete()
                return redirect("home")
        else:
            return redirect("login")
    else:
        return redirect("login")

#The function that renders the page with all the user favourite articles and recipies
def favourites(request):
    if not request.user.is_authenticated:
        return redirect("login")

    context = {}
    articles = []
    recipes = []

    favourites = Favourite.objects.filter(user=request.user)

    for f in favourites:
        if f.article:
            articles.append(f.article)
        if f.recipe:
            recipes.append(f.recipe)

    context["articles"] = articles
    context["recipes"] = recipes

    return render(request, "main/favourites.html", context)

#The function that take user search criteria such as contenttype(articles or or tags)
#search value (title of an article or a recipe) and tags and returns the articles and/or recipes
#that match these criteria
def search(request):
    # Filters if favourite content is requested
    favourite = str(request.GET.get("favourite"))

    if favourite == "True" and request.user.is_authenticated:
        articles = []
        recipes = []
        favour = Favourite.objects.filter(user=request.user)

        for f in favour:
            if f.article:
                articles.append(f.article)
            if f.recipe:
                recipes.append(f.recipe)
    else:
        articles = Article.objects.all()
        recipes = Recipe.objects.all()

    # Fetches tag object for each tag listed in the GET request
    contenttags = request.GET.getlist("tags")
    tags = [Tag.objects.get(title=tag).id for tag in contenttags]

    query = str(request.GET.get("q")) # uses q for user search query
    contenttype = request.GET.getlist("type") or []

    context = {"query": query or "Search", "recipes": [], "articles": []}

    # Fetch recipes and articles, filtered by content and tags
    if "articles" in contenttype:
        if tags:
            context["articles"].extend(articles.filter(title__icontains=query, tag__id__in=tags))
        else:
            context["articles"].extend(articles.filter(title__icontains=query))
    if "recipes" in contenttype:
        if tags:
            context["recipes"].extend(recipes.filter(title__icontains=query, tag__id__in=tags))
        else:
            context["recipes"].extend(recipes.filter(title__icontains=query))

    print(context)

    return render(request, "main/search.html", context)

#The function that renders the page with all the faqs from the db
def faq(request):
    context = {
        'faqs': Faq.objects.all(),
    }
    return render(request, "main/faq.html", context)
