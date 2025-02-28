// scripts.js

document.addEventListener("DOMContentLoaded", function() {
    console.log("Document loaded");
    
});

function toggleMenu() {
    const navMenu = document.querySelector(".nav-list");
    navMenu.classList.toggle("active");
}


$(document).ready(function() {
    $('#logout-button').click(function(event) {
        event.preventDefault(); // Prevent default behavior

        let logoutUrl = $(this).data("logout-url"); // Get logout URL from button

        $.ajax({
            type: 'POST',
            url: logoutUrl,  
            headers: { "X-CSRFToken": getCookie('csrftoken') }, // Send CSRF token
            success: function(response) {
                window.location.href = response.redirect_url; // Redirect user
            },
            error: function(xhr, status, error) {
                alert('Logout failed. Please try again.');
            }
        });
    });
});

// Function to get CSRF token from cookies
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


    document.addEventListener("DOMContentLoaded", function() {
    fetch("/api/pharmacist/prescriptions/", {
        headers: {
            "Authorization": "Bearer " + localStorage.getItem("token"),
        },
    })
    .then(response => response.json())
    .then(data => {
        const prescriptionList = document.getElementById("prescription-list");
        prescriptionList.innerHTML = "";

        data.forEach(consultation => {
            const item = document.createElement("li");
            item.innerHTML = `
                <strong>${consultation.patient_name}</strong>: ${consultation.prescriptions}
                (Prescribed by Dr. ${consultation.doctor_name}) 
                <button class="serve-btn" data-id="${consultation.id}">Mark as Served</button>
            `;
            prescriptionList.appendChild(item);
        });

        document.querySelectorAll(".serve-btn").forEach(button => {
            button.addEventListener("click", function() {
                const consultationId = this.getAttribute("data-id");
                fetch(`/api/pharmacist/prescriptions/${consultationId}/serve/`, {
                    method: "PATCH",
                    headers: {
                        "Authorization": "Bearer " + localStorage.getItem("token"),
                        "Content-Type": "application/json",
                    },
                })
                .then(response => response.json())
                .then(data => {
                    alert(data.message);
                    this.parentElement.remove(); // Remove item from list after serving
                })
                .catch(error => console.error("Error:", error));
            });
        });
    })
    .catch(error => console.error("Error fetching prescriptions:", error));
});