from django.shortcuts import redirect
from livres.models import Profile

class EtablissementMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            try:
                profile = Profile.objects.get(user=request.user)
                request.user_etablissement = profile.etablissement
                request.user_role = profile.role
            except Profile.DoesNotExist:
                request.user_etablissement = None
                request.user_role = None
        else:
            request.user_etablissement = None
            request.user_role = None
        
        return self.get_response(request)