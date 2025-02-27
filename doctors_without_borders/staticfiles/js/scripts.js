// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("Document loaded");
    
});

function toggleMenu() {
    const navMenu = document.querySelector(".nav-list");
    navMenu.classList.toggle("active");
}



document.getElementById("login-form").addEventListener("submit", function(event) {
    event.preventDefault();
    
    let username = document.getElementById("username").value;
    let password = document.getElementById("password").value;

    fetch("/api/login/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Login successful!");
            window.location.href = "/";  // Redirect to homepage
        } else {
            alert("Invalid credentials");
        }
    })
    .catch(error => console.error("Error:", error));
});


document.getElementById("register-form").addEventListener("submit", function(event) {
    event.preventDefault();

    let username = document.getElementById("reg-username").value;
    let email = document.getElementById("reg-email").value;
    let password = document.getElementById("reg-password").value;

    fetch("/api/auth/register/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username: username, email: email, password: password })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            alert("Registration successful!");
            window.location.href = "/login";
        } else {
            alert("Error registering: " + JSON.stringify(data));
        }
    })
    .catch(error => console.error("Error:", error));
});


$(document).ready(function() {
    $('#logout-button').click(function(event) {
        event.preventDefault(); // Prevent the default form submission

        $.ajax({
            type: 'POST',
            url: '{% url "logout" %}', // Adjust the URL as necessary
            data: {
                'csrfmiddlewaretoken': '{{ csrf_token }}' // Include CSRF token
            },
            success: function(response) {
                // Handle successful logout
                window.location.href = response.redirect_url; // Redirect to login or home page
            },
            error: function(xhr, status, error) {
                // Handle errors
                alert('Logout failed. Please try again.');
            }
        });
    });
});

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
            xhr.setRequestHeader("X-CSRFToken", '{{ csrf_token }}');
        }
    }
});

fetch('user/logout/', {
    method: 'POST',
    headers: { 'X-CSRFToken': getCookie('csrftoken') }  // Ensure CSRF token is included
})
.then(response => response.json())
.then(data => {
    window.location.href = data.redirect_url;  // Redirect user to login page
})
.catch(error => console.error('Error:', error));

// Function to get CSRF token from cookies (if needed)
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        document.cookie.split(';').forEach(cookie => {
            let trimmedCookie = cookie.trim();
            if (trimmedCookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(trimmedCookie.split('=')[1]);
            }
        });
    }
    return cookieValue;
}

function markAsRead(event, notificationId) {
        event.preventDefault(); // Prevent the page from refreshing
       
        const notificationElement = document.querySelector(`li[data-id='${notificationId}']`);
        
        // Send an AJAX request to mark the notification as read
        fetch(`/notifications/read/${notificationId}/`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value,
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                notificationElement.classList.remove('unread');
                notificationElement.classList.add('read');
            }
        })
        .catch(error => console.error('Error marking notification as read:', error));
    }
