document.addEventListener("DOMContentLoaded", function () {
    console.log("🚀 Pharmacist Dashboard JS Loaded!");

    fetch("/pharmacist/prescriptions/")
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            console.log("✅ Prescriptions Data:", data);  // Log the data structure

            const prescriptionList = document.getElementById("pharmacist-prescriptions"); // Update the ID to match the correct one
            prescriptionList.innerHTML = ""; // Clear any existing content

            // Check if prescriptions data is available
            if (data.prescriptions && data.prescriptions.length > 0) {
                data.prescriptions.forEach(prescription => {
                    const listItem = document.createElement("li");
                    listItem.innerHTML = `
                        <strong>Patient:</strong> ${prescription.patient} <br>
                        <strong>Doctor:</strong> ${prescription.doctor} <br>
                        <strong>Prescriptions:</strong> ${prescription.prescriptions} <br>
                    `;
                    prescriptionList.appendChild(listItem);
                });
            } else {
                prescriptionList.innerHTML = "<li>No prescriptions available.</li>"; // If no data is available
            }
        })
        .catch(error => {
            console.error("❌ Error fetching prescriptions:", error);
            const prescriptionList = document.getElementById("pharmacist-prescriptions");
            prescriptionList.innerHTML = "<li>Error loading prescriptions.</li>";
        });
});