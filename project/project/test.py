from datetime import datetime
from django.test import TestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
class Hosttest(TestCase):
    
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.live_server_url = 'http://127.0.0.1:8000/'

    def tearDown(self):
        self.driver.quit()
        
    def test_01_login_page(self):
        driver = self.driver
        driver.get(self.live_server_url)
        driver.maximize_window()
        time.sleep(1)
        login=driver.find_element(By.CSS_SELECTOR,"i.fa.fa-fw.fa-user.text-light.mr-1")
        login.click()

        login=driver.find_element(By.CSS_SELECTOR,"a.dropdown-item[href='/register/login/']")
        login.click()
        time.sleep(2)
        email = driver.find_element(By.CSS_SELECTOR, "input[name='email'][id='your_email']")
        email.send_keys("ria@gmail.com")

        # Find and fill in the password field
        password = driver.find_element(By.CSS_SELECTOR, "input[name='password'][id='your_pass']")
        password.send_keys("Ria@12")

        # Wait for a few seconds to ensure the form is ready
        time.sleep(2)

        # Find and click the login button
        submit = driver.find_element(By.CSS_SELECTOR, "input[name='signin'][id='signin']")
        submit.click()

        # Wait for the login process to complete
        time.sleep(2)
        home=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/']")
        home.click()
        time.sleep(2)
        shop=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/shop/']")
        shop.click()
        time.sleep(2)
        cart=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-success.text-white[href='/add_to_cart/3/']")
        cart.click()
        time.sleep(2)
        cart_view=driver.find_element(By.CSS_SELECTOR,"i.fa.fa-fw.fa-cart-arrow-down.text-light.mr-1")
        cart_view.click()
        time.sleep(2)
        cart_exit=driver.find_element(By.CSS_SELECTOR,"a[href='/shop']:contains('←')")
        cart_exit.click()
        time.sleep(2)
        wish=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-success.text-white.wishlist-button#wishlist-button")
        wish.click()
        time.sleep(2)
        home2=driver.find_element(By.CSS_SELECTOR,"a.nav-link[href='/']")
        home2.click()
        time.sleep(2)
        wish_view=driver.find_element(By.CSS_SELECTOR,"a.btn.btn-success i.fas.fa-heart")
        wish_view.click()
        time.sleep(2)

        

        
        
        
        
        
        
        
        
        
if __name__ == '__main__':
    import unittest
    unittest.main()