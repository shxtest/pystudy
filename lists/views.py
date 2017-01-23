from django.shortcuts import render,redirect
from lists.models import Item


# Create your views here.

def home_page(request):     # 首页视图
    if request.method == 'POST':
        Item.objects.create(text=request.POST['item_text'])
        return redirect('/lists/the-only-list-in-the-world/')         # 重定向
#    items = Item.objects.all()
    return render(request, 'home.html')


def view_list(request):     # 单个清单视图
    items = Item.objects.all()
    return render(request, 'list.html', {'items': items})
