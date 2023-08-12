from django.urls import reverse
from django.shortcuts import redirect


class AuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        auth_required_urls = [
            reverse('cinema_schedule'),
        ]

        # Check if the request URL is in the auth_required_urls list and if the user is not authenticated
        if request.path in auth_required_urls and not request.user.is_authenticated:
            return redirect('login_user')

        response = self.get_response(request)
        return response
