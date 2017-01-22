#! python3

from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time
from django.test import LiveServerTestCase


class NewVisitorTest(LiveServerTestCase):
#初始化浏览器
    def setUp(self):
        
        self.driver = webdriver.Ie()
#        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)      #隐式等待时间

#关闭浏览器        
    def tearDown(self):
        
        self.driver.quit()
        
#重构功能测试
    def CheckForRowInListTable(self, row_text):
        table = self.driver.find_element_by_id('id_list_table')
        
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn(row_text, [row.text for row in rows])
        
#测试用例
    def test_CanStartAListAndRetrieveItLater(self):
#打开网页应用
        self.driver.get(self.live_server_url)
        
        self.assertIn('To-Do',self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

#她做事很有条理
        inputbox = self.driver.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
# 她按回车键后，页面更新了
# 待办事项表格中显示了"1: Buy peacock feathers"
        inputbox.send_keys('Buy peacock feathers')
        
        inputbox.send_keys(Keys.ENTER)
        self.CheckForRowInListTable('1: Buy peacock feathers')
        
#页面中还有一个文本，可以输入其他的待办事项
#她输入了:Use peacock feathers to make a fly
#她做事很有条理
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

#页面再次更新，清单中显示了这2个待办事项
        self.CheckForRowInListTable('2: Use peacock feathers to make a fly')
        self.CheckForRowInListTable('1: Buy peacock feathers')
        

# 她想知道这个网站是 否会记住她的清单
# 她看到网站为她生成了一个唯一的URL
# 页面中有一些文字解决这个功能
        self.fail('Finish the test!')       #提醒测试结束

# 她访问那个URL，发现待办事项清单还在

    
        
