from django.shortcuts import redirect

class OnboardingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated and request.user.first_time_login and request.path != '/onboarding/':
            return redirect('onboarding')

        return self.get_response(request)