from django.db import models
from django.contrib.auth.models import User

class Fanfic(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    content = models.TextField(default='Текст фанфика будет здесь.')
    rating = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='fanfic_images/', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title