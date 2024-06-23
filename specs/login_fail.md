## Login Fail

arrange:

- open http://localhost:5173/login

act:

- fill data-test-id:email-input with "user"
- fill data-test-id:password-input with "password"
- click data-test-id:submit-button
- read data-test-id:message-label

assert:

- data-test-id:message-label should be "Invalid Username or Password"
