## Login Labels

arrange:

- open http://localhost:5173/login

act:

- read data-test-id:emal-label
- read data-test-id:password-label
- read data-test-id:submit-button

assert:

- data-test-id:email-label should be "Email or Username"
- data-test-id:password-label should be "Password"
- data-test-id:submit-button should be "Submit"
