from django.urls import path
from .views import SignUp, LogOut

urlpatterns = [
    path('signup', SignUp.as_view(), name='signup'),
    path('logout', LogOut.as_view(), name='logout'),
]