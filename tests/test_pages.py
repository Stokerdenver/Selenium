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
# Один должен быть выбран, второй НЕ выбран
def test_checkboxes_page(browser):
    browser.get("https://the-internet.herokuapp.com/checkboxes")
    checkboxes = browser.find_elements("css selector", "input[type='checkbox']")
    assert not checkboxes[0].is_selected(), "Checkbox 1 должен быть снят"
    assert checkboxes[1].is_selected(), "Checkbox 2 должен быть выбран"

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


# Проходим критический путь пользователя:
# Логин -> Выбор и добавление товара в корзину -> 
# переброс пользователя в корзину -> оплата товара
def test_user_can_complete_purchase(browser):
    browser.get("https://www.saucedemo.com/")
    
    name_input = browser.find_element(By.ID, "user-name")
    name_input.send_keys("standard_user")

    pass_input = browser.find_element(By.ID, "password")
    pass_input.send_keys("secret_sauce")
    
    browser.find_element(By.ID, "login-button").click()

    WebDriverWait(browser, 10).until(
        EC.element_to_be_clickable((By.ID, "add-to-cart-sauce-labs-backpack"))
    )

    browser.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    cart_badge = browser.find_element(By.CLASS_NAME, "shopping_cart_badge")

#   Проверяем, что счетчик корзины стал 1 после добавления товара
    assert cart_badge.text == "1", f"ОШИБКА: ожидали '1', а получили '{cart_badge.text}'"

    browser.find_element(By.CSS_SELECTOR, "a[class='shopping_cart_link']").click()
    browser.find_element(By.CSS_SELECTOR, "button[class='btn btn_action btn_medium checkout_button ']").click()
    
    customer_name_input = browser.find_element(By.ID, "first-name")
    custmoer_last_name_input= browser.find_element(By.ID, "last-name")
    zip_code_input = browser.find_element(By.ID, "postal-code")

    customer_name_input.send_keys("Serega")
    custmoer_last_name_input.send_keys("BrutalGuy")
    zip_code_input.send_keys("0143")

    browser.find_element(By.CSS_SELECTOR, "input[class='submit-button btn btn_primary cart_button btn_action']").click()
    browser.find_element(By.ID, "finish").click()

    assert browser.current_url == "https://www.saucedemo.com/checkout-complete.html"
    
# Тестируем работу с JavaScript Alerts
# Окна, которые вылезают с вопросом, например, точно хотите покинуть сайт ? 
# Чтобы понять - попробуйте сами: https://the-internet.herokuapp.com/javascript_alerts
def test_js_alerts_is_working(browser):
    browser.get("https://the-internet.herokuapp.com/javascript_alerts")

    browser.find_element(By.CSS_SELECTOR, "button[onclick='jsAlert()']").click()
    # Переключаемся на алерт
    alert = browser.switch_to.alert

    # Проверяем текст
    assert alert.text == "I am a JS Alert"

    # Подтверждаем (нажимаем OK)
    alert.accept()

    # Проверяем результат на странице
    result = browser.find_element(By.ID, "result").text
    assert result == "You successfully clicked an alert"

# Тестируем ожидание загрузки чего-либо на странице 
# Ждём, пока не появится надпись "Hello, World !"
def test_is_load_complete(browser):
    browser.get("https://the-internet.herokuapp.com/dynamic_loading/1")

    browser.find_element(By.ID, "start").click()

    # Ждем, пока *что-то* грузится
    # Для этого ждем исчезновения элемента с изображением загрузки
    # (в данном случае - это гифка с загрузкой)
    WebDriverWait(browser, 10).until(
         EC.invisibility_of_element_located((By.CSS_SELECTOR, "img[src='/img/ajax-loader.gif']"))
     )
    
     # Ждём, пока появится текст Hello World
    finish_elem = WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.ID, "finish"))
    )
    assert finish_elem == "Hello World !", "Текст не совпадает с ожидаемым"
    










