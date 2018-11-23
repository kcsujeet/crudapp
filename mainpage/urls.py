from django.urls import path, include
from mainpage.views import *

urlpatterns = [

    path('', homeview,name="home"),
    path('delete/<task_id>/', deletetask, name="delete"),
    path('signup/', signup, name="signup"),
    path('accounts/', include('django.contrib.auth.urls')),
    path('profile/', update_profile, name="update_profile")

]
