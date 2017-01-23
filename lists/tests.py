from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item


# Create your tests here.
# 为首页视图编写单元测试
class HomePageTest(TestCase):
# 通过'/'指向首页home_page
    def test_RootUrlResolveToHomePageView(self):
        found = resolve('/')
# 判断由视图的哪个函数处理请求
        self.assertEqual(found.func, home_page)

# 测试首页返回正确的html:
#      判断返回内容是否以<html>开头
#      判断返回内容的标题是否有To-Do lists
#      判断返回内容是否以</html>结尾
    def test_HomePageReturnsCorrectHtml(self):
        request = HttpRequest()    
        response = home_page(request)

# 测试模板是否正确渲染
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)


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


# 使用Django测试客户端client
class ListviewTest(TestCase):
# 检查是否使用了不同模板
    def test_uses_list_template(self):
        response = self.client.get('/lists/the-only-list-in-the-world/')
        self.assertTemplateUsed(response, 'list.html')


    def test_displays_all_items(self):
        Item.objects.create(text='itemey 1')
        Item.objects.create(text='itemey 2')

        response = self.client.get('/lists/the-only-list-in-the-world/')

        self.assertContains(response, 'itemey 1')
        self.assertContains(response, 'itemey 2')


class NewListTest(TestCase):

    def test_save_a_post_request(self):
        self.client.get('/lists/new', data={'item_text': 'A new list item'})         # 使用client重写post请求

        self.assertEqual(Item.objects.count(), 1)  # 检查是否把Item对象存入数据库
        new_item = Item.objects.first()  # 等价于 objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')  # 检查待办事项的text是否正确

# 检查处理请求返回的状态，及重定向是否正确
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})     # 使用client重写post请求
        self.assertRedirects(response, '/lists/the-only-list-in-the-world/')


        
    


        
        
