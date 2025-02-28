document.getElementById("register-form").addEventListener("submit", async function(event) {
    event.preventDefault();

    let formData = new FormData(this);

    try {
        let response = await fetch('/api/register/', {
            method: 'POST',
            body: formData  // Do NOT manually set Content-Type; FormData handles it
        });

        let data = await response.json();
        
        if (response.ok) {
            alert(data.message);
            window.location.href = '/onboarding';  // Redirect to onboarding page
        } else {
            console.error('Registration failed:', data);
            alert(`Error: ${data.error || "Registration failed. Please check your inputs."}`);
        }
    } catch (error) {
        console.error('Network or server error:', error);
        alert("A network error occurred. Please try again.");
    }
});