from django.urls import include, path
from rest_framework.routers import SimpletRouter

from .views import (CommentViewSet, ReviewViewSet)

v1_router = SimpletRouter()
#Другие urls
v1_router.register(r'titles/(?P<title_id>\d+)/reviews',
                ReviewViewSet, basename='reviews')
v1_router.register(r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)'
                r'/comments', CommentViewSet, basename='comments')

urlpatterns = [
    path('v1/', include(v1_router.urls)),
    #другие urls
]
