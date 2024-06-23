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
