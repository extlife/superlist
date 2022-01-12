from django.urls import path
from . import views

app_name = 'lists'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('lists/the-one-of-a-kind-list-in-the-world/', views.view_list,
        name='view_list'),
]