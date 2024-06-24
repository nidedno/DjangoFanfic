from django.shortcuts import render, redirect, get_object_or_404
from .models import Fanfic, Chapter
from .forms import FanficForm, SearchForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.template import RequestContext

def home(request):
    fanfics = Fanfic.objects.all()[:10]
    return render(request, 'fanfic/home.html', {'fanfics': fanfics})

@login_required
def create_fanfic(request):
    if request.method == 'POST':
        form = FanficForm(request.POST, request.FILES)
        if form.is_valid():
            fanfic = form.save(commit=False)
            fanfic.user = request.user
            fanfic.save()

            # Разбиение описания на главы по 1000 символов
            content = fanfic.content
            chapters = [content[i:i + 1000] for i in range(0, len(content), 1000)]
            for i, chapter_content in enumerate(chapters):
                Chapter.objects.create(fanfic=fanfic, title=f'Глава {i + 1}', content=chapter_content)

            return redirect('my_fanfics')
    else:
        form = FanficForm()
    return render(request, 'fanfic/create_fanfic.html', {'form': form})

@login_required
def my_fanfics(request):
    fanfics = Fanfic.objects.filter(user=request.user)
    return render(request, 'fanfic/my_fanfics.html', {'fanfics': fanfics})

def fanfic_detail(request, pk):
    fanfic = get_object_or_404(Fanfic, pk=pk)
    return render(request, 'fanfic/fanfic_detail.html', {'fanfic': fanfic})

def chapter_detail(request, fanfic_pk, chapter_pk):
    fanfic = get_object_or_404(Fanfic, pk=fanfic_pk)
    chapter = get_object_or_404(Chapter, pk=chapter_pk)
    chapters = list(fanfic.chapters.all())
    current_index = chapters.index(chapter)
    prev_chapter = chapters[current_index - 1] if current_index > 0 else None
    next_chapter = chapters[current_index + 1] if current_index < len(chapters) - 1 else None
    context = {
        'fanfic': fanfic,
        'chapter': chapter,
        'prev_chapter': prev_chapter,
        'next_chapter': next_chapter,
    }
    return render(request, 'fanfic/chapter_detail.html', context)


def increase_rating(request, pk):
    fanfic = get_object_or_404(Fanfic, pk=pk)
    fanfic.rating += 1
    fanfic.save()
    return redirect('fanfic_detail', pk=pk)

@login_required
def delete_fanfic(request, pk):
    fanfic = get_object_or_404(Fanfic, pk=pk)
    if fanfic.user == request.user:
        fanfic.delete()
    return redirect('my_fanfics')

def search_fanfics(request):
    if request.method == 'GET':
        form = SearchForm(request.GET)
        if form.is_valid():
            query = form.cleaned_data['query']
            fanfics = Fanfic.objects.filter(tags__icontains=query)
            return render(request, 'fanfic/search_results.html', {'fanfics': fanfics})
    else:
        form = SearchForm()
    return render(request, 'fanfic/search_fanfics.html', {'form': form})

def search_results(request):
    query = request.GET.get('q')
    fanfics = Fanfic.objects.filter(tags__icontains=query)
    return render(request, 'fanfic/search_results.html', {'fanfics': fanfics})

def contact(request):
    if request.method == 'POST':
        message_name = request.POST['name']
        message_email = request.POST['email']
        message = request.POST['message']

        send_mail(
            'Сообщение с сайта',
            message,
            message_email,
            ['nidedno@gmail.com'],
        )

        return render(request, 'fanfic/contact.html', {'message_name': message_name})
    else:
        return render(request, 'fanfic/contact.html')

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return render(request, 'registration/logout_confirm.html')

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def handler404(request, exception):
    response = render('404.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 404
    return render(request, '404.html')

def handler500(request):
    response = render('500.html', {},
                              context_instance=RequestContext(request))
    response.status_code = 500
    return render(request, '500.html')