from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item

# Create your tests here.
#为首页视图编写单元测试
class HomePageTest(TestCase):
#通过'/'指向首页home_page
    def test_RootUrlResolveToHomePageView(self):
        found = resolve('/')
#判断由视图的哪个函数处理请求
        self.assertEqual(found.func, home_page)


#测试首页返回正确的html:
 #      判断返回内容是否以<html>开头
 #      判断返回内容的标题是否有To-Do lists
 #      判断返回内容是否以</html>结尾
    def test_HomePageReturnsCorrectHtml(self):
        request = HttpRequest()    
        response = home_page(request)

#测试模板是否正确渲染
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

#检查返回的HTML中是否有新添加的待办事项
    def test_HomePageCanSaveAPostRequest(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(Item.objects.count(), 1)       #检查是否把Item对象存入数据库
        new_item = Item.objects.first()     # 等价于 objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')      # 检查待办事项的text是否正确

# 检查处理请求返回的状态，及重定向是否正确        
    def test_HomePageRedirectsAfterPOST(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response['location'], '/')     

# 一个测试只测一件事
    def test_HomePageOnlySavesItemsWhennecessary(self):
        request = HttpRequest()
        home_page(request)
        self.assertEqual(Item.objects.count(), 0)
        
# 检查模板是否能显示多个待办事项
    def test_HomePageDisplaysAllListItems(self):
        Item.objects.create(text = 'itemey 1')
        Item.objects.create(text = 'itemey 2')

        request = HttpRequest()
        response = home_page(request)

        self.assertIn('itemey 1', response.content.decode())
        self.assertIn('itemey 2', response.content.decode())      
        
# 定义ItemModelTest（）方法
class ItemModelTest(TestCase):
    def test_SavingAndRetrievingItems(self):
        item_1 = Item()
        item_1.text = '第一个ever list item'
        item_1.save()
        
        item_2 = Item()
        item_2.text = '第二个ever list item'
        item_2.save()

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, '第一个ever list item')
        self.assertEqual(second_saved_item.text, '第二个ever list item')

        
    


        
        
