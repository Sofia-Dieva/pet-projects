from . models import Recipe
from django.forms import ModelForm, TextInput, Textarea


class RecipeForm(ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'description']
        widgets = {
            'title': TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Write title'
            }),
            'description': Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write description'
            })
        }
