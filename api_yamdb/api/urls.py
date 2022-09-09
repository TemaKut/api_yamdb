from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router_v1 = SimpleRouter()

router_v1.register('titles', views.TitleViewSet, basename='titles')
router_v1.register('categories', views.CategoryViewSet, basename='categories')
router_v1.register('genres', views.GenreViewSet, basename='genres')


urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
