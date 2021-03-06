from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.

def home_page(request):
    '''Home page'''
    return render(request, 'lists/home.html')

def view_list(request, list_id):
    '''List view'''
    list_ = List.objects.get(id=list_id)
    return render(request, 'lists/list.html', {'list': list_})

def new_list(request):
    '''New list'''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

def add_item(request, list_id):
    '''Add item'''
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect(f'/lists/{list_.id}/')

