from django.urls import path
from news.views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete
from django.views.decorators.cache import cache_page

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>/', cache_page(60*10), PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
