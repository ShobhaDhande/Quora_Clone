from django.urls import path
from .views import LoginView,SignupView,LogOutView


urlpatterns = [
    path('', LoginView.as_view(),name='login'),
    path('signup/',SignupView.as_view(), name='signup'),
    path('logout/',LogOutView.as_view(), name='logout')
]