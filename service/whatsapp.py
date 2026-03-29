from hashlib import md5

from selenium import webdriver
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from .base import BaseMessangerFirefoxSession
from .dataclasses import ChatData


class WhatsappSession(BaseMessangerFirefoxSession):
    url = 'https://web.whatsapp.com'

    def __init__(self, user_id, proifles_path):
        super().__init__(user_id, proifles_path)

    def enter(self):
        self.driver.get(self.url)            

    def set_login_status(self, timeout=30):
        if not self.is_inside_messanger():
            self.enter()
        
        element = self._wait_for_element(timeout, By.XPATH, "/html/body/div[1]/div/div/div/div/div[3]/div/div[4]/header/header/div/div/h2/span/span/span/span")
        if element is not None:  
            self.is_logged_in = True
    
    def is_inside_messanger(self):
        return self.driver.current_url.find(self.url) >= 0

    def login(self, phone_number, *args, **kwargs):       
        self.set_login_status()
        if self.is_logged_in:
            return {
                'message': 'You are already logged in.',
                'phone_number': phone_number
            }
        else:
            return self._login_by_phone_number(phone_number)
        
    def get_user_info(self, *args, **kwargs):
        return super().get_user_info(*args, **kwargs)
    
    def _login_by_phone_number(self, phone_number):
        # Wait for loading QR element
        element = self._wait_for_element(90, By.CSS_SELECTOR, '._akaz')
        if not element:
            raise TimeoutException('Unable to open QR so we can\'t open sign in by phone number')

        # Get log in with phone number link
        element = self._wait_for_element(10, By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div[2]/div[2]/div[2]/div/div/div[1]')
        element.click()
        
        # Insert phone number into the input field
        element = self._wait_for_element(30, By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div[1]/div[2]/div/div/div/form/input')
        element.clear()
        element.send_keys(phone_number)
        
        # Locate the login button
        element = self._wait_for_element(10, By.XPATH, '/html/body/div[1]/div/div/div/div/div[2]/div[2]/div[1]/div/div/div[3]/div[3]/button')
        element.click()

        # Get code for logging into the account
        element = self._wait_for_element(30, By.CSS_SELECTOR, '[aria-details="link-device-phone-number-code-screen-instructions"]')
        print(element)
        data_element = element.get_dom_attribute('data-link-code') or ''
        print('Data element', data_element)
        
        all_attributes = self.driver.execute_script('var items = {}; for (index = 0; index < arguments[0].attributes.length; ++index) { items[arguments[0].attributes[index].name] = arguments[0].attributes[index].value }; return items;', element)

        print(all_attributes)
        data_element = data_element.replace(',', '')
        data_element = data_element[:4] + '-' + data_element[4:]

        return {
            'message': f'Insert into your phone this code to log in: {data_element}',
            'value': data_element
        }

    def get_chats(self, *args, **kwargs):
        self.set_login_status()
        if(self.is_logged_in):
            # Get chat rows
            chats_list = self._wait_for_element(40, By.XPATH, '//*[@id="pane-side"]/div[1]/div/div')
            chat_elements = chats_list.find_elements(By.CSS_SELECTOR, '.x10l6tqk.xh8yej3.x1g42fcv')
            chats = []
            for el in chat_elements:
                try:
                    name_el = el.find_element(By.CSS_SELECTOR, '.xuxw1ft.x6ikm8r.x10wlt62.xlyipyv.x78zum5')
                    chats.append(
                        ChatData(
                            name=name_el.text
                        )
                    )
                except NoSuchElementException as e:
                    print('No element here', e)
            
            return chats
        else:
            return {'error': 'You aren\'t logged in'}

    def get_contacts(self, *args, **kwargs):
        return super().get_contacts(*args, **kwargs)

    def get_messages(self, *args, **kwargs):
        return super().get_messages(*args, **kwargs)
    
    def logout(self):
        return super().logout()