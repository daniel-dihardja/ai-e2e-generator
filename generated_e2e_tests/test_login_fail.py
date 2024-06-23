from selenium.webdriver.common.by import By
from web_driver import get_driver

def test_login_fail():
    driver = get_driver()
    try:
        # Arrange: Set up the test
        driver.get("http://localhost:5173/login")

        # Act: Perform the actions
        driver.find_element(By.CSS_SELECTOR, "[data-test-id='email-input']").send_keys("user")
        driver.find_element(By.CSS_SELECTOR, "[data-test-id='password-input']").send_keys("password")
        driver.find_element(By.CSS_SELECTOR, "[data-test-id='submit-button']").click()
        message_label = driver.find_element(By.CSS_SELECTOR, "[data-test-id='message-label']").text.strip()

        # Assert: Verify the results
        expected_message_label_text = "Invalid Username or Password"
        assert message_label == expected_message_label_text, f"Expected '{expected_message_label_text}', but got '{message_label}'"

    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    test_login_fail()
