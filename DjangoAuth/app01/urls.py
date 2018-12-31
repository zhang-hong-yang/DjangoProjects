from django.urls import path
from .views import *
urlpatterns = [

    path('login/', login),
    path('logout/', logout),
    path('index/', index),

]