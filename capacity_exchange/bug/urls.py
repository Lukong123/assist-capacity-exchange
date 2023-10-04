from django.urls import path
from .views import *

urlpatterns = [
    path("", IndexView.as_view(), name = "index"),
    path("<int:pk>/", DetailView.as_view(), name="detail"),
    path("register-bug/", RegisterBugView.as_view(), name="register-bug")
]