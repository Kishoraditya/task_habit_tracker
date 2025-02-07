import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

@pytest.fixture(scope="module")
def driver():
    options = Options()
    options.add_argument("--headless")
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

def test_responsive_layout(driver):
    # Replace with your local or deployed URL
    url = "http://localhost:8000"
    driver.get(url)
    # Test on different screen sizes:
    sizes = [(320, 480), (768, 1024), (1366, 768)]
    for width, height in sizes:
        driver.set_window_size(width, height)
        # Wait a little for layout to settle
        driver.implicitly_wait(2)
        # Assert that the title is correct      
        assert driver.title == "Task & Habit Tracker"
