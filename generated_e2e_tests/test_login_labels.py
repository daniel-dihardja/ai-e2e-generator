from selenium.webdriver.common.by import By
from web_driver import get_driver

def test_login_labels():
    driver = get_driver()
    try:
        # Arrange: Set up the test
        driver.get("http://localhost:5173/login")

        # Act: Perform the actions
        email_label = driver.find_element(By.CSS_SELECTOR, "[data-test-id='email-label']")
        actual_email_label_text = email_label.text.strip()

        password_label = driver.find_element(By.CSS_SELECTOR, "[data-test-id='password-label']")
        actual_password_label_text = password_label.text.strip()

        submit_button = driver.find_element(By.CSS_SELECTOR, "[data-test-id='submit-button']")
        actual_submit_button_text = submit_button.text.strip()

        # Assert: Verify the results
        expected_email_label_text = "Email or Username"
        assert actual_email_label_text == expected_email_label_text, f"Expected '{expected_email_label_text}', but got '{actual_email_label_text}'"

        expected_password_label_text = "Password"
        assert actual_password_label_text == expected_password_label_text, f"Expected '{expected_password_label_text}', but got '{actual_password_label_text}'"

        expected_submit_button_text = "Submit"
        assert actual_submit_button_text == expected_submit_button_text, f"Expected '{expected_submit_button_text}', but got '{actual_submit_button_text}'"

    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    test_login_labels()
