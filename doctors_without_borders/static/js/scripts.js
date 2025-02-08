// scripts.js
document.addEventListener("DOMContentLoaded", function() {
    console.log("Static files loaded successfully!");

    const messageBox = document.getElementById("message-box");
    if (messageBox) {
        setTimeout(() => {
            messageBox.style.display = "none";
        }, 3000); // Hide messages after 3 seconds
    }
});