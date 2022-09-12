from django.urls import include, path

from rest_framework import routers

from . import views

app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register(
    r'users', views.CertainUser, basename='users_certain'
)
router_v1.register(r'users', views.GetOrCreateUsers, basename='users')

router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    views.ReviewViewSet, basename='reviews'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
    r'/comments', views.CommentViewSet, basename='comments'
)


urlpatterns = [
    path('v1/users/me/', views.users_me, name='users_me'),
    path('v1/auth/token/', views.GetCustomToken.as_view(), name='get_token'),
    path(
        'v1/auth/signup/', views.EmailConfirm.as_view(), name='get_conf_code'
    ),
    path('v1/', include(router_v1.urls)),
]
