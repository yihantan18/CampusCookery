from .models import UserProfile
from .models import Tag

# Adds user_profile to the context
def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = UserProfile.objects.get(user=request.user)
        except UserProfile.DoesNotExist:
            profile = None
        return {'user_profile': profile}
    return {'user_profile': None}

# Add tags to the context
def tags(request):
    return {'tags': Tag.objects.all()}
