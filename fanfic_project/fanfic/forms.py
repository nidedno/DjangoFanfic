from django import forms
from .models import Fanfic

class FanficForm(forms.ModelForm):
    class Meta:
        model = Fanfic
        fields = ['title', 'description', 'content', 'image']

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск по тегам', max_length=100)