from django.urls import include, path
from rest_framework import routers

from . import views

app_name = 'api'

router_v1 = routers.SimpleRouter()
router_v1.register(
    r'users', views.CertainUser, basename='users_certain')
router_v1.register(r'users', views.GetOrCreateUsers, basename='users')

router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('users/me/', views.users_me, name='users_me'),
    path('auth/token/', views.GetCustomToken.as_view(), name='get_token'),
    path('auth/signup/', views.EmailConfirm.as_view(), name='get_conf_code'),
]
