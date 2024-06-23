import os
import re
import sys
from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
import utils

load_dotenv(override=True)

template = """
You are an expert in writing E2E (end-to-end) tests for web applications using Selenium. 
I want you to generate the E2E tests for a web application based on the following specifications:

<test_specs>
{specs}
</test_specs>

Please generate the Python code for the E2E test using the following structure:

<example>
from selenium.webdriver.common.by import By
from web_driver import get_driver

def test_email_label():
    driver = get_driver()
    try:
        # Arrange: Set up the test
        driver.get("http://localhost:9999/lpath")

        # Act: Perform the actions
        email_label = driver.find_element(By.CSS_SELECTOR, "[data-test-id='email-label']")
        actual_label_text = email_label.text.strip()

        # Assert: Verify the results
        expected_email_label_text = "Email"
        assert actual_email_label_text == expected_email_label_text, f"Expected '[expected_email_label_text]', but got '[actual_email_label_text]'"

    finally:
        # Clean up
        driver.quit()

if __name__ == "__main__":
    test_email_label()
</example>

Instructions:
- Keep the imports exactly as they are. Do not add or remove any import statements.
- Use the H2 title from the specs for the name of the test function. (e.g., ## Email Label -> def test_email_label():)
- Translate each line in the 'arrange' section into a corresponding Selenium command. (e.g., - open http://localhost:5173/login -> driver.get("http://localhost:5173/login"))
- Translate each line in the 'act' section into a corresponding Selenium command to interact with elements by their data-test-id attribute. 
  (e.g., - fill data-test-id:email-input with "user" -> driver.find_element(By.CSS_SELECTOR, "[data-test-id='email-input']").send_keys("user"))
  (e.g., - click data-test-id:submit-button -> driver.find_element(By.CSS_SELECTOR, "[data-test-id='submit-button']").click())
  (e.g., - read data-test-id:message-label -> message_label = driver.find_element(By.CSS_SELECTOR, "[data-test-id='message-label']").text.strip())
  (e.g., - read url -> current_url = driver.current_url)
- Translate each line in the 'assert' section into a corresponding assert statement. 
  (e.g., - data-test-id:message-label should be "Invalid Username or Password" -> expected_message_label_text = "Invalid Username or Password" and assert actual_message_label_text == expected_message_label_text, f"Expected '{{expected_message_label_text}}', but got '{{actual_message_label_text}}'")
  (e.g., - url should be "http://localhost:5173/welcome" -> expected_url = "http://localhost:5173/welcome" and assert current_url == expected_url, f"Expected '{{expected_url}}', but got '{{current_url}}'")
- Return the generated code as a string without saving it to a file.

Do not add any other answers, explanations, or comments. Just generate the Python code for the E2E test based on the provided specifications.
"""

def generate_e2e_test(spec_file):
    prompt_template = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model=os.getenv('OPENAI_MODEL'), api_key=os.getenv('OPENAI_API_KEY'))
    chain = prompt_template | llm
    spec = utils.read_md_file(spec_file)
    print(spec)
    res = chain.invoke({"specs": spec})
    code = res.content
    cleaned_code = re.sub(r'```python\n|```', '', code, flags=re.MULTILINE)
    file_name = utils.generate_filename_from_h2(spec)
    utils.write_to_file(f"generated_e2e_tests/{file_name}", cleaned_code)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Error: Missing spec file. Please specify a spec file as an argument.\nUsage: python ai_e2e_tests_generator.py <spec_file>")
        sys.exit(1)
    
    spec_file = sys.argv[1]
    generate_e2e_test(spec_file)