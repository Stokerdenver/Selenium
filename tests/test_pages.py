import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Сайты для тестирования:
# Моковый магазин одежды: https://www.saucedemo.com/
# Моковый сайт с различными формами и кнопками: https://the-internet.herokuapp.com/




# Проверка заголовка страницы
def test_title(browser):
    browser.get("https://the-internet.herokuapp.com/inputs")
    assert browser.title == "The Internet"

# Работа с инпутами, пишем в текстбокс значение, потом проверяем, записалось ли 
def test_input_field(browser):
    browser.get("https://the-internet.herokuapp.com/inputs")
    input_elem = browser.find_element("tag name", "input")
    input_elem.send_keys("123")
    assert input_elem.get_attribute("value") == "123"

# Работа с чек-боксами
def test_checkboxes_page(browser):
    browser.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = browser.find_elements("css selector", "input[type='checkbox']")
    assert len(checkboxes) == 2

# Работа с формой логина
def test_reg_form(browser):
    browser.get("https://www.saucedemo.com/")

    name_input = browser.find_element(By.ID, "user-name")
    name_input.send_keys("standard_user")

    pass_input = browser.find_element(By.ID, "password")
    pass_input.send_keys("secret_sauce")
    
    browser.find_element(By.ID, "login-button").click()

    assert browser.current_url == "https://www.saucedemo.com/inventory.html"

# Работа с изображениями
def test_image_loaded(browser):
    browser.get("https://www.saucedemo.com/")
    browser.find_element(By.ID, "user-name").send_keys("standard_user")
    browser.find_element(By.ID, "password").send_keys("secret_sauce")
    browser.find_element(By.ID, "login-button").click()

    # Ждём появления картинки
    img = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CSS_SELECTOR, "img[alt='Sauce Labs Backpack']"))
    )

    # Проверка загрузки
    # complete — браузер завершил загрузку картинки
    # naturalWidth > 0 — у изображения есть ширина, то есть оно не пустое/битое
    loaded = browser.execute_script(
        "return arguments[0].complete && arguments[0].naturalWidth > 0", img
    ) 
    assert loaded, "Изображение не загрузилось"



