from django.shortcuts import render, redirect
from lists.models import Item

# Create your views here.

def home_page(request):
    '''Home page'''
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/')
    items = Item.objects.all()
    return render(request, 'lists/home.html', {'items': items})
