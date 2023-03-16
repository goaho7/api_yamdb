from django.urls import include, path

from .views import SignupView, TokenView


urlpatterns = [
    path('v1/auth/signup/', SignupView.as_view(), name='signup'),
    path('v1/auth/token/', TokenView.as_view(), name='token'),
]
