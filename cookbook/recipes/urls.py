from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome_page, name='welcome'),
    path('accounts/signup', views.SignUpView.as_view(), name='signup'),
    path('addnew', views.addnew, name='addnew'),
    path('post/<int:pk>/', views.ShowRecipe.as_view(), name='post'),
    path('recipes', views.page_with_recipes, name='recipes')
]
