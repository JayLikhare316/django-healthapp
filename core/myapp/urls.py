from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="index"),
    path('about',views.about,name="about"),
    path('bmi',views.bmi,name="bmi"),
    path('calculator',views.calculator,name="calculator"),
    path('signup',views.signup,name="signup"),
    path('signin',views.signin,name="signin"),
    path('chat_app',views.chat_app,name="chat_app"),
    path('logout_user',views.logout_user,name="logout_user"),
    path('dietplan',views.dietplanview,name="dietplan"),



]
