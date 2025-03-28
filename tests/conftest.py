import pytest
from selenium import webdriver

@pytest.fixture
def browser(request):
    driver = webdriver.Chrome()
    yield driver

    # Проверка, сработал ли хук и был ли провал
    if hasattr(request.node, "rep_call") and request.node.rep_call.failed:
        test_name = request.node.name
        driver.save_screenshot(f"screenshots/{test_name}.png")
        print(f"\n Скриншот сохранён: screenshots/{test_name}.png")

    driver.quit()

# Хук для фиксации результатов выполнения
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Получаем результат выполнения теста (setup/call/teardown)
    outcome = yield
    rep = outcome.get_result()
    setattr(item, f"rep_{rep.when}", rep)  # item.rep_call, item.rep_setup и т.д.
