// registration.js

document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();

    const formData = new FormData(event.target);
    
    fetch('/api/register/', {
        method: 'POST',
        body: formData,
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert(data.message);
            window.location.href = '/onboarding';  // Redirect to onboarding page
        } else {
            alert("Registration failed. Please try again.");
        }
    })
    .catch(error => console.error('Error:', error));
});