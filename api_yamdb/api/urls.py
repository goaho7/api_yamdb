from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                       ReviewViewSet, SignupView, TitleViewSet, TokenView,
                       UserViewSet)

router_v1 = DefaultRouter()

router_v1.register(r'categories', CategoryViewSet)
router_v1.register(r'genres', GenreViewSet)
router_v1.register(r'titles', TitleViewSet)

router_v1.register(r'users', UserViewSet, basename='users')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments'
)

auth_urls = [
    path('signup/', SignupView.as_view(), name='signup'),
    path('token/', TokenView.as_view(), name='token'),
]

urlpatterns = [
    path('v1/', include(router_v1.urls)),
    path('v1/auth/', include(auth_urls)),
]
