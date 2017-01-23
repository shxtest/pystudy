from django.shortcuts import render,redirect
from lists.models import Item


# Create your views here.

def home_page(request):     # 首页视图
    return render(request, 'home.html')


# 单个清单视图
def view_list(request):
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})


# 新清单列表视图
def new_list(request):
    Item.objects.create(text=request.POST['item_text'])
    return redirect('/lists/the-only-list-in-the-world/')

