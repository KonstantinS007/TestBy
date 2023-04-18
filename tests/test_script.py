from selenium.webdriver.support.wait import WebDriverWait
import time
from selenium.webdriver.support import expected_conditions as EC
import pytest
from selenium import webdriver as selenium_webdriver
from selenium.webdriver.chrome.options import Options


@pytest.fixture(scope='session')
def selenium_driver():
    chrome_options = Options()
    # chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    driver = selenium_webdriver.Chrome(executable_path=r"chromedriver",
                                       options=chrome_options)
    driver.set_window_size(1920, 1080)
    driver.maximize_window()
    driver.implicitly_wait(5)

    # логинимся
    driver.get('http://petfriends.skillfactory.ru/login')
    time.sleep(3)
    emal = ('id', "email")
    passd = ('id', "pass")
    button = ('xpath', "//button[contains(text(),'Войти')]")  # 'xpath', "//button[contains(text(),'Войти')]"  'css_selector', 'button[type="submit"]'
    driver.find_element(*emal).send_keys("123@a.ru")
    driver.find_element(*passd).send_keys("123@a.ru")
    time.sleep(3)
    origin = WebDriverWait(driver, 7).\
        until(EC.presence_of_element_located(button), message=f"Not find {button}")
    origin.click()
    yield driver

    driver.quit()


def test_show_my_pets(selenium_driver):
    ''' Тест на проверку списка питомцев:
       1. Проверяем, что оказались на странице питомцев пользователя.
       2. Проверяем, что присутствуют все питомцы.  '''

    driver = selenium_driver
    # driver.get("https://petfriends.skillfactory.ru/login")
    # Нажимаем на кнопку входа в пункт меню Мои питомцы
    locator0 = ('xpath', "//a[contains(text(),'Мои питомцы')]")  # By.CSS_SELECTOR, "a.nav-link[href='/my_pets']"
    origin = driver.find_element(*locator0)
    origin.click()
    time.sleep(3)
    # Проверяем, что оказались на странице питомцев пользователя
    assert driver.current_url == 'https://petfriends.skillfactory.ru/my_pets'

    # 1. Проверяем, что присутствуют все питомцы, для этого:
    # находим кол-во питомцев по статистике пользователя и проверяем, что их число
    # соответствует кол-ву питомцев в таблице
    locator1 = ('xpath', '//div[@class=".col-sm-4 left"]')
    pets_number = driver.find_element(*locator1).text.split('\n')[1].split(': ')[1]
    # pets_count = 100
    locator2 = ('xpath', '//table[@class="table table-hover"]/tbody/tr')
    pets_count = driver.find_elements(*locator2)
    assert int(pets_number) == len(pets_count)
