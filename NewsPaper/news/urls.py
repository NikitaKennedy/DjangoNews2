from accounts.views import SignUp, LogOut
from django.urls import path
from news.views import PostsList, PostDetail, PostSearch, PostCreate, PostUpdate, PostDelete

urlpatterns = [
    path('', PostsList.as_view(), name='news'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('search/', PostSearch.as_view(), name='search'),
    path('add/', PostCreate.as_view(), name='post_create'),
    path('login/', SignUp.as_view(),  name='login' ),
    path('logout/', LogOut.as_view(), name='logout' ),
    path('<int:pk>/edit/', PostUpdate.as_view(), name='post_update'),
    path('<int:pk>/delete/', PostDelete.as_view(), name='post_delete'),
]
