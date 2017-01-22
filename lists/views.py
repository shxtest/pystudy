from django.shortcuts import render,redirect
from lists.models import Item


# Create your views here.

def home_page(request):
    if request.method == 'POST':
        Item.objects.create(text = request.POST['item_text'])
        return redirect('/')         # 重定向

    items = Item.objects.all()
    return render(request, 'home.html', {'items': items})
    
def home(request):
    pass
    

    
