document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Pharmacist Dashboard JS Loaded!");

    const prescriptionList = document.getElementById("pharmacist-prescriptions");

    if (!prescriptionList) {
        console.error("❌ Error: Element with ID 'pharmacist-prescriptions' not found.");
        return;
    }

    fetch("/pharmacist/prescriptions/")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ Prescriptions Data:", data);
            prescriptionList.innerHTML = ""; // Clear existing content

            if (data.prescriptions && data.prescriptions.length > 0) {
                data.prescriptions.forEach(prescription => {
                    const listItem = document.createElement("li");
                    listItem.innerHTML = `
                        <strong>Patient:</strong> ${prescription.patient} <br>
                        <strong>Doctor:</strong> ${prescription.doctor} <br>
                        <strong>Prescriptions:</strong> ${prescription.prescriptions} <br>
                        <button class="mark-served-btn" data-id="${prescription.id}">Mark as Served</button>
                    `;
                    prescriptionList.appendChild(listItem);
                });

                // Add event listeners to "Mark as Served" buttons
                document.querySelectorAll(".mark-served-btn").forEach(button => {
                    button.addEventListener("click", function () {
                        const prescriptionId = this.getAttribute("data-id");
                        markAsServed(prescriptionId, this);
                    });
                });
            } else {
                prescriptionList.innerHTML = "<li>No prescriptions available.</li>";
            }
        })
        .catch(error => {
            console.error("❌ Error fetching prescriptions:", error);
            prescriptionList.innerHTML = "<li>Error loading prescriptions.</li>";
        });
});

// Function to handle "Mark as Served"
document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Pharmacist Dashboard JS Loaded!");

    document.querySelectorAll(".mark-served-btn").forEach(button => {
        button.addEventListener("click", function () {
            const prescriptionId = this.getAttribute("data-id");

            fetch(`/pharmacist/prescriptions/${prescriptionId}/serve/`, {
                method: "PATCH",  // Ensure it matches your Django view
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCSRFToken() // Django CSRF protection
                },
                body: JSON.stringify({ served: true })
            })
            .then(response => {
                if (!response.ok) {
                    throw new Error("Failed to update prescription.");
                }
                return response.json();
            })
            .then(data => {
                console.log("✅ Prescription marked as served:", data);

                // Update button state dynamically
                button.innerHTML = `<i class="fas fa-check-circle"></i> Served`;
                button.classList.remove("btn-success");
                button.classList.add("btn-secondary");
                button.disabled = true;
            })
            .catch(error => {
                console.error("❌ Error updating prescription:", error);
                alert("Error marking prescription as served. Please try again.");
            });
        });
    });

    // Function to get CSRF Token
    function getCSRFToken() {
        return document.querySelector('[name=csrfmiddlewaretoken]').value;
    }
});

// Function to get CSRF token for Django
function getCSRFToken() {
    const csrfToken = document.cookie.match(/csrftoken=([^ ;]+)/);
    return csrfToken ? csrfToken[1] : "";
}