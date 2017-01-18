from django.test import TestCase
from django.core.urlresolvers import resolve
from lists.views import home_page
from django.http import HttpRequest
from django.template.loader import render_to_string

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
        
        #self.assertTrue(response.content.startswith(b'<html>'))      
        #self.assertIn(b'<title>To-Do lists</title>',response.content)   
        #self.assertTrue(response.content.endswith(b'</html>'))

#测试模板是否正确渲染
        expected_html = render_to_string('home.html')
        self.assertEqual(response.content.decode(), expected_html)

#检查返回的HTML中是否有新添加的待办事项
    def test_HomePageCanSaveAPostRequest(self):
        request = HttpRequest()
        request.method = 'POST'
        request.POST['item_text'] = 'A new list item'

        response = home_page(request)
        self.assertIn('A new list item', response.content.decode())
        
