from django.urls import path
from .views import PostList, PostDetail, PostListSearch

urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>', PostDetail.as_view()),
    path('search/', PostListSearch.as_view() )
    ]