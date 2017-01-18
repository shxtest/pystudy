#! python3

from selenium import webdriver
import unittest
from selenium.webdriver.common.keys import Keys
import time


class NewVisitorTest(unittest.TestCase):
#初始化浏览器
    def setUp(self):
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(3)      #隐式等待时间

#关闭浏览器        
    def tearDown(self):
        self.driver.quit()
#测试用例
    def test_CanStartAListAndRetrieveItLater(self):
        self.driver.get('http://127.0.0.1:8000')
        self.assertIn('To-Do',self.driver.title)
        header_text = self.driver.find_element_by_tag_name('h1').text
        self.assertIn('To-Do',header_text)

#通过id定位输入框
        inputbox = self.driver.find_element_by_id('id_new_item')
        self.assertEqual(
            inputbox.get_attribute('placeholder'),
            'Enter a to-do item'
            )
# 输入信息，并按回车键
        inputbox.send_keys('Buy peacock feathers')
        inputbox.send_keys(Keys.ENTER)
#扩充复制代码，检查添加的第2个待办事项
        inputbox = self.driver.find_element_by_id('id_new_item')
        inputbox.send_keys('Use peacock feathers to make a fly')
        inputbox.send_keys(Keys.ENTER)

        #time.sleep(5)
        table = self.driver.find_element_by_id('id_list_table')
        rows = table.find_elements_by_tag_name('tr')
        self.assertIn('1: Buy peacock feathers', [row.text for row in rows])
        self.assertIn('2: Use peacock feathers to make a fly',
                      [row.text for row in rows])

        self.fail("完成测试")       #提醒测试结束


if __name__ == '__main__':
    unittest.main(warnings = 'ignore')
    
        
