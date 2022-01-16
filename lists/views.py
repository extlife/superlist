from django.shortcuts import render, redirect
from lists.models import Item, List

# Create your views here.

def home_page(request):
    '''Home page'''
    return render(request, 'lists/home.html')

def view_list(request):
    '''List view'''
    items = Item.objects.all()
    return render(request, 'lists/list.html', {'items': items})

def new_list(request):
    '''New list'''
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)
    return redirect('/lists/the-one-of-a-kind-list-in-the-world/')
