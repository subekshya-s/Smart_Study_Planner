const form = document.getElementById('login-form');

form.addEventListener('submit', function(event) {
    event.preventDefault();

    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;

    if (username === '' || password === '') {
        document.getElementById('error-msg').textContent = 'Username and password are required';
        document.getElementById('error-msg').style.display = 'block';
        return;
    }

    fetch('http://127.0.0.1:8000/api/auth/login/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            username: username,
            password: password,
        })
    })
    .then(function(response) {
        return response.json();
    })
    .then(function(data) {
        if (data.access) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            window.location.href = 'smart.html';
        } else {
            document.getElementById('error-msg').textContent = 'Invalid username or password';
            document.getElementById('error-msg').style.display = 'block';
        }
    })
    .catch(function(error) {
        document.getElementById('error-msg').textContent = 'Something went wrong. Is the server running?';
        document.getElementById('error-msg').style.display = 'block';
    });
});