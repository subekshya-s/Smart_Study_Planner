// Step 1: Find the form in HTML
const form = document.getElementById('register-form');

// Step 2: Listen for when user submits the form
form.addEventListener('submit', function(event) {

    // Step 3: Stop the page from reloading
    event.preventDefault();

    // Step 4: Grab what the user typed
    const username = document.getElementById('username').value;
    const email = document.getElementById('email').value;
    const password = document.getElementById('password').value;

    // Step 5: Frontend validation - don't even call API if fields empty
    if (username === '' || password === '') {
        document.getElementById('error-msg').textContent = 'Username and password are required';
        document.getElementById('error-msg').style.display = 'block';
        return; // stop here, don't go further
    }

    // Step 6: Call the Django API
    fetch('http://127.0.0.1:8000/api/auth/register/',  {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json', // tell Django we're sending JSON
        },
        body: JSON.stringify({ // convert JS object to JSON string
            username: username,
            email: email,
            password: password,
        })
    })

    // Step 7: Convert the response to JSON
    .then(function(response) {
        return response.json();
    })

    // Step 8: Handle the response
    .then(function(data) {
        if (data.access) {
            // Success - save tokens and go to dashboard
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            window.location.href = 'smart.html'; // redirect
        } else {
            // API returned an error e.g. username taken
            document.getElementById('error-msg').textContent = JSON.stringify(data);
            document.getElementById('error-msg').style.display = 'block';
        }
    })

    // Step 9: Handle network errors e.g. server not running
    .catch(function(error) {
        document.getElementById('error-msg').textContent = 'Something went wrong. Is the server running?';
        document.getElementById('error-msg').style.display = 'block';
    });

});