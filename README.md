# AI E2E Generator

AI E2E Generator allows you to write end-to-end test specifications in a simple, descriptive markdown format and leverages LangChain to interact with the OpenAI language model for generating comprehensive E2E test scripts in Python. This tool streamlines the process of creating Selenium-based tests, making it easier and more efficient to maintain robust test coverage for your web applications.

## Example Usage

Construct your markdown by defining the test case with an H2 title, which becomes the function name in the generated Python code. The markdown entries are divided into three sections following the Arrange, Act, Assert (AAA) approach:

- **Arrange**: Setup the initial state of the test, such as opening a specific URL.
- **Act**: Perform actions like filling out forms or clicking buttons.
- **Assert**: Verify the expected outcomes to ensure the application behaves as intended.

By using this approach, you are automatically adhering to the AAA testing pattern, ensuring clear and maintainable tests.

Here’s an example markdown specification:

```markdown
## Login Success

arrange:

- open http://http://localhost:5173/login

act:

- fill data-test-id:email-input with "admin"
- fill data-test-id:password-input with "password"
- click data-test-id:submit-button
- read url
- read data-test-id:welcome-title

assert:

- url should be "http://localhost:5173/welcome"
- data-test-id:welcome-title should be "Welcome"
```

The E2E Python code can then be generated from the markdown specification using this Makefile command:

```shell
make generate_e2e_test spec_file=specs/login_success.md
```

And here's the resulting Python code from the markdown specification:

```python
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
```

## Implementation Details

The core of AI E2E Generator is based on prompt engineering techniques to guide the AI in generating the correct test scripts from markdown specifications. Here's a deeper look into how this is achieved:

#### Prompt Engineering

Prompt engineering is the process of designing and refining prompts to elicit the desired response from an AI model. In this project, prompt engineering plays a crucial role in transforming markdown specifications into executable Python code.

1.**Template Creation**: A detailed prompt template is created to instruct the AI on how to interpret the markdown specification and generate the corresponding Python code. This template includes examples and specific instructions to ensure accuracy and consistency.

```python
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
```

2. **Markdown Parsing**: The markdown specification is parsed to extract the relevant sections (Arrange, Act, Assert). Each section is then transformed into corresponding Selenium commands using the prompt template.

3. **AI Integration**: The LangChain library is used to interact with the OpenAI language model, passing the constructed prompt and receiving the generated Python code.

````python
def generate_e2e_test(spec_file):
    prompt_template = PromptTemplate.from_template(template)
    llm = ChatOpenAI(model=os.getenv('OPENAI_MODEL'), api_key=os.getenv('OPENAI_API_KEY'))
    chain = prompt_template | llm
    spec = utils.read_md_file(spec_file)
    res = chain.invoke({"specs": spec})
    code = res.content
    cleaned_code = re.sub(r'```python\n|```', '', code, flags=re.MULTILINE)
    file_name = utils.generate_filename_from_h2(spec)
    utils.write_to_file(f"generated_e2e_tests/{file_name}", cleaned_code)
````

4. **Output Generation**: The resulting Python code is cleaned and saved to a file for execution.

## Conclusion

AI E2E Generator leverages the power of AI through prompt engineering to automate the generation of end-to-end tests from simple markdown specifications. This approach not only saves time but also ensures consistency and maintainability in your test suites.
