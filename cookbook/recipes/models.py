from django.db import models


# Create your models here.
class Recipe(models.Model):
    title = models.CharField('Title', max_length=50)
    description = models.TextField('Description')

    def __str__(self):
        return self.title
