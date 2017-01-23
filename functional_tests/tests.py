#! python3

from selenium import webdriver
# import unittest
from selenium.webdriver.common.keys import Keys
# import time
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
# 初始化浏览器
    def setUp(self):
        self.driver = webdriver.Ie()
        self.driver.implicitly_wait(10)      # 隐式等待时间

# 关闭浏览器
    def tearDown(self):
        self.driver.quit()
        
# 重构功能测试
    def CheckForRowInListTable(self, row_text):
        table = self.driver.find_element_by_id('id_list_table')
        
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])

# 测试用例
    def test_CanStartAListAndRetrieveItLater(self):
# 打开网页应用
        self.driver.get(self.live_server_url)
        
        self.assertIn('To-Do',self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

# 她做事很有条理
        inputbox = self.driver.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )

        inputbox.send_keys('Buy peacock feathers')

# 她按回车键后，页面更新了
# 待办事项表格中显示了"1: Buy peacock feathers"       
        inputbox.send_keys(Keys.ENTER)
        edith_list_url = self.driver.current_url
        self.assertRegex(edith_list_url, '/lists/.+')
        self.CheckForRowInListTable('1: Buy peacock feathers')
        
# 页面中还有一个文本，可以输入其他的待办事项
# 她输入了:Use peacock feathers to make a fly
# 她做事很有条理
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

# 页面再次更新，清单中显示了这2个待办事项
        self.CheckForRowInListTable('2: Use peacock feathers to make a fly')
        self.CheckForRowInListTable('1: Buy peacock feathers')
        
# 现在有一个新用户访问了网站

## 使用一个新浏览器会话
## 确保前一个用户的信息不会从cookie中泄露出去
        self.driver.quit()
        self.driver = webdriver.Ie()

# 新用户访问首页
# 页面中看不到前一个用户的清单
        self.driver.get(self.live_server_url)
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertNotIn('make a fly', page_text)
        
# 新用户输入1个新待办事项，新建一个清单
# 新用户不像前一个用户那样兴趣盎然
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Buy milk')
        inputbox.send_keys(Keys.ENTER)

# 新用户获得了唯一的URL
        new_list_url = self.driver.current_url
        self.assertRegex(new_list_url, '/lists/.+')
        self.assertNotIn(new_list_url, edith_list_url)
        
# 这个页面还是没有前一个用户的清单
        page_text = self.driver.find_element_by_tag_name('body').text
        self.assertNotIn('Buy peacock feathers', page_text)
        self.assertIn('Buy milk', page_text)
        
# 大家都很满意，去睡觉了
