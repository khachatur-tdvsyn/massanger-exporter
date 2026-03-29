
from abc import ABC, abstractmethod
from pathlib import Path

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.webdriver import LocalWebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait

class BaseMessangerSession(ABC):
    url: str

    def __init__(self, session_id: str):
        self.session_id = session_id
        self.is_logged_in = False
    
    @abstractmethod
    def login(self, *args, **kwargs):
        ...

    @abstractmethod
    def get_chats(self, *args, **kwargs):
        ...
    
    @abstractmethod
    def get_messages(self, *args, **kwargs):
        ...
    
    @abstractmethod
    def get_contacts(self, *args, **kwargs):
        ...
    
    @abstractmethod
    def logout(self):
        ...

class BaseMessangerFirefoxSession(BaseMessangerSession, ABC):
    def __init__(self, session_id, proifles_path):
        super().__init__(session_id)
        self.profiles_path = Path(proifles_path)
        self.driver : LocalWebDriver = None
        self._init_webdriver()
    
    def _wait_for_element(self, timeout, by, value) -> WebElement | None:
        element = None
        try:
            wait = WebDriverWait(self.driver, timeout)
            element = wait.until(lambda driver: driver.find_element(by, value))
        except TimeoutException as e:
            print('Waiting for the element timed out')
        finally:
            return element
    
    @classmethod
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_value, traceback):
        self.driver.quit()
    
    def _init_webdriver(self):
        options = webdriver.FirefoxOptions()

        # options.add_argument("--headless")
        options.add_argument("--profile")

        profile_path = self.profiles_path / str(self.session_id or 0)
        if not profile_path.exists():
            profile_path.mkdir()

        print(str(profile_path))
        options.add_argument(str(profile_path))

        geckodriver_path = "/snap/bin/geckodriver"  # specify the path to your geckodriver
        driver_service = webdriver.FirefoxService(executable_path=geckodriver_path)

        self.driver = webdriver.Firefox(options=options, service=driver_service)