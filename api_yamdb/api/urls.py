from django.urls import include, path
from rest_framework.routers import SimpleRouter

from . import views

app_name = 'api'

router_v1 = SimpleRouter()

# router_v1.register('posts', views.PostsViewSet, basename='posts')

urlpatterns = [
    # path('v1/', include('djoser.urls.jwt')),
    # path('v1/', include(router_v1.urls)),
]
