from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create/', views.create_fanfic, name='create_fanfic'),
    path('my_fanfics/', views.my_fanfics, name='my_fanfics'),
    path('fanfic/<int:pk>/', views.fanfic_detail, name='fanfic_detail'),
    path('fanfic/<int:pk>/delete/', views.delete_fanfic, name='delete_fanfic'),
    path('fanfic/<int:pk>/rate/', views.increase_rating, name='increase_rating'),
    path('search/', views.search_fanfics, name='search_fanfics'),
    path('search/results/', views.search_results, name='search_results'),
    path('contact/', views.contact, name='contact'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

handler404 = 'fanfic.views.handler404'
handler500 = 'fanfic.views.handler500'