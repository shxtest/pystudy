from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.

def home_page(request):
#返回请求的html,title标签，自行构建HttpResponse对象
    #return HttpResponse('<html><title>To-Do lists</title></html>')

#重构home.html后，使用django.render()请求返回的页面
#    return render(request, 'home.html')

#    if request.method == 'POST':
#        return HttpResponse(request.POST['item_text'])

    return render(request, 'home.html',{
        'new_item_text': request.POST.get('item_text', ''),
        })
    
def home(request):
    pass
    

    
