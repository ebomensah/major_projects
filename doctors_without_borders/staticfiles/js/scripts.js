// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("Document loaded");
    
});

function toggleMenu() {
        const navMenu = document.querySelector("nav ul");
        navMenu.classList.toggle("active");
}

document.getElementById("logout-button").addEventListener("click", function (e) {
    e.preventDefault();

    fetch("/api/auth/logout/", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCSRFToken(),  // Include CSRF Token
            "X-Requested-With": "XMLHttpRequest"
        }
    }).then(response => response.json())
      .then(data => {
          console.log(data.message);
          window.location.href = "/login/";  // Redirect to login page
      }).catch(error => console.error("Error:", error));
});

// Function to get CSRF Token from Cookies
function getCSRFToken() {
    const cookieValue = document.cookie
        .split("; ")
        .find(row => row.startsWith("csrftoken="))
        ?.split("=")[1];
    return cookieValue || "";
}

// Function to get CSRF token from cookies
function getCSRFToken() {
    let cookieValue = null;
    if (document.cookie) {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith("csrftoken=")) {
                cookieValue = cookie.substring("csrftoken=".length);
                break;
            }
        }
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
