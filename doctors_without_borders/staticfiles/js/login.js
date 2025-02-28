document.addEventListener("DOMContentLoaded", function() {
    const loginForm = document.getElementById("login-form");
    
    if (loginForm) {
        loginForm.addEventListener("submit", function(event) {
            event.preventDefault();
            
            let username = document.getElementById("username").value;
            let password = document.getElementById("password").value;
            
            fetch("/api/login/", {  // Adjust this URL to your API
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify({ username: username, password: password })
            })
            .then(response => response.json())
            .then(data => {
                if (data.redirect_url) {
                    window.location.href=data.redirect_url;
                    alert("Login successful!");
                } else {
                    alert("Invalid credentials");
                }
            })
            .catch(error => console.error("Error:", error));
        });
    }
});
