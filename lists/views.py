from django.shortcuts import render, redirect
from lists.models import Item, List


# Create your views here.

def home_page(request):     # 首页视图
    return render(request, 'home.html')


# 清单视图，支持多个清单，用id区分唯一性
def view_list(request, list_id):
    list_ = List.objects.get(id=list_id)
    items = Item.objects.filter(list=list_)
    return render(request, 'list.html', {'items': items})


# 新清单列表视图
def new_list(request):
    list_ = List.objects.create()
    Item.objects.create(text=request.POST['item_text'], list=list_)     # 保存新建的待办事项
    return redirect('/lists/%d/' % (list_.id,))


# 新增待办事项视图
def add_item(request, list_id):
    list_ = List.objects.get(id=list_id)
    Item.objects.create(text=request.POST['item_text'], list=list_)     # 保存新建的待办事项
    return redirect('/lists/%d/' % (list_.id,))