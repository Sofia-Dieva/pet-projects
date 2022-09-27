from django.shortcuts import render, redirect
from .models import Recipe
from .forms import RecipeForm
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic
from django.views.generic.detail import DetailView


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'


def welcome_page(request):
    return render(request, 'recipes/main_page.html')


class ShowRecipe(DetailView):
    model = Recipe
    template_name = 'recipes/recipe_detail.html'
    pk_url_kwarg = 'pk'


def page_with_recipes(request):
    add = list(Recipe.objects.all())
    return render(request, 'recipes/recipebook.html', {'title': 'Add new recipe', 'add': add})


def addnew(request):
    error = ''
    if request.method == 'POST':
        form = RecipeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('recipes')
        else:
            error = 'Your form is incorrect'

    form = RecipeForm
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'recipes/addnewrecipe.html', context)
