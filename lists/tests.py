from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string
from lists.models import Item, List


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


# 测试Item、List模型
class ListAndItemModelTest(TestCase):
    def test_saving_and_retrieving_items(self):
        list_ = List()
        list_.save()

        first_item = Item()
        first_item.text = 'The first (ever) list item'
        first_item.list = list_     # 把待办事项first_item归到List名下
        first_item.save()

        second_item = Item()
        second_item.text = 'The second (ever) list item'
        second_item.list = list_    # 把待办事项second_item归到List名下
        second_item.save()

        saved_list = List.objects.first()       #
        self.assertEqual(saved_list, list_)     # 检查清单是否保存正确

        saved_items = Item.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_saved_item = saved_items[0]
        second_saved_item = saved_items[1]
        self.assertEqual(first_saved_item.text, 'The first (ever) list item')    # 检查待办事项first_item与清单的关系
        self.assertEqual(first_saved_item.list, list_)
        self.assertEqual(second_saved_item.text, 'The second (ever) list item')  # 检查待办事项second_item与清单的关系
        self.assertEqual(second_saved_item.list, list_)


# 使用Django测试客户端client
class ListviewTest(TestCase):
# 检查是否使用了不同模板
    def test_uses_list_template(self):
        list_ = List.objects.create()
        response = self.client.get('/lists/%d/' % (list_.id,))
        self.assertTemplateUsed(response, 'list.html')

    def test_displays_only_items_for_that_list(self):
        correct_list = List.objects.create()
        Item.objects.create(text='itemey 1', list=correct_list)
        Item.objects.create(text='itemey 2', list=correct_list)

        other_list = List.objects.create()
        Item.objects.create(text='other list item 1', list=other_list)
        Item.objects.create(text='other list item 2', list=other_list)

        response = self.client.get('/lists/%d/' % (correct_list.id,))
        self.assertContains(response, 'itemey 1')       # 期望在当前清单中显示的待办事项
        self.assertContains(response, 'itemey 2')
        self.assertNotContains(response, 'other list item 1')   # 不期望在当前清单中显示的待办事项
        self.assertNotContains(response, 'other list item 2')


class NewListTest(TestCase):
    def test_save_a_post_request(self):
        self.client.post('/lists/new', data={'item_text': 'A new list item'})         # 使用client重写post请求
        self.assertEqual(Item.objects.count(), 1)  # 检查是否把Item对象存入数据库
        new_item = Item.objects.first()  # 等价于 objects.all()[0]
        self.assertEqual(new_item.text, 'A new list item')  # 检查待办事项的text是否正确

# 检查处理请求返回的状态，及重定向是否正确
    def test_redirects_after_POST(self):
        response = self.client.post('/lists/new', data={'item_text': 'A new list item'})     # 使用client重写post请求
        new_list = List.objects.first()
        self.assertRedirects(response, '/lists/%d/' % (new_list.id,))       # 检查重定向的页面是否是新list


class NewItemTest(TestCase):
    def test_can_save_a_POST_request_to_an_existing_list(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        self.client.post('/lists/%d/add_item' % (correct_list.id,),
                         data={'item_text': 'A new item for an existing list'})
        self.assertEqual(Item.objects.count(), 1)  # 检查是否把Item对象存入数据库

        new_item = Item.objects.first()
        self.assertEqual(new_item.text, 'A new item for an existing list')      # 检查新待办事项的text是否正确
        self.assertEqual(new_item.list, correct_list)       # 检查新待办事项是否加入到现有清单

    def test_redirects_to_list_view(self):
        correct_list = List.objects.create()
        other_list = List.objects.create()

        response = self.client.post('/lists/%d/add_item' % (correct_list.id,),
                                    data={'item_text': 'A new item for an existing list'})
        self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))  # 检查重定向的页面是否是当前清单页面




        
    


        
        
