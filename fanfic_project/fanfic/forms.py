from django import forms
from .models import Fanfic

class FanficForm(forms.ModelForm):
    class Meta:
        model = Fanfic
        fields = ['title', 'description', 'content', 'image', 'tags']
        widgets = {
            'content ': forms.Textarea(attrs={'rows':1, 'cols':1}),
        }

    def __init__(self, *args, **kwargs):
        super(FanficForm, self).__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class SearchForm(forms.Form):
    query = forms.CharField(label='Поиск по тегам', max_length=100)