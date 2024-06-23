from selenium.webdriver.common.by import By
from web_driver import get_driver

def test_login_success():
    driver = get_driver()
    try:
        # Arrange: Set up the test
        driver.get("http://localhost:5173/login")

        # Act: Perform the actions
        driver.find_element(By.CSS_SELECTOR, "[data-test-id='email-input']").send_keys("admin")
        driver.find_element(By.CSS_SELECTOR, "[data-test-id='password-input']").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, "[data-test-id='submit-button']").click()
        current_url = driver.current_url
        welcome_title = driver.find_element(By.CSS_SELECTOR, "[data-test-id='welcome-title']").text

        # Assert: Verify the results
        expected_url = "http://localhost:5173/welcome"
        assert current_url == expected_url, f"Expected '{expected_url}', but got '{current_url}'"
        expected_welcome_title = "Welcome"
        assert welcome_title == expected_welcome_title, f"Expected '{expected_welcome_title}', but got '{welcome_title}'"

    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    test_login_success()