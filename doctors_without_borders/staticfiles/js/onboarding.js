document.addEventListener("DOMContentLoaded", function() {
    console.log("🚀 JavaScript Loaded!");

    function toggleField(choiceFieldId, targetFieldId) {
        let choiceField = document.getElementById(choiceFieldId);
        let targetField = document.getElementById(targetFieldId);

        function updateVisibility() {
            targetField.style.display = (choiceField.value === 'Yes') ? 'block' : 'none';
        }

        if (choiceField && targetField) {
            choiceField.addEventListener('change', updateVisibility);
            updateVisibility(); 
        }
    }

    toggleField('id_allergies', 'id_allergies_detail');
    toggleField('id_chronic_disease_status', 'id_chronic_disease_detail');
    toggleField('id_smoking_status', 'id_smoking_detail');
    toggleField('id_alcohol_status', 'id_alcohol_detail');

    // Screenings
    const prostateScreening = document.getElementById('prostate-screening');
    const cervicalScreening = document.getElementById('cervical-cancer-screening');
    const breastScreening = document.getElementById('breast-cancer-screening');

    const genderField = document.getElementById('id_gender');
    const ageField = document.getElementById('id_age');

    function updateScreeningVisibility() {
        const gender = genderField ? genderField.value.trim() : "";
        const age = ageField ? parseInt(ageField.value, 10) || 0 : 0;

        console.log("🟢 Gender:", gender);
        console.log("🟢 Age:", age);

        // Show/hide screening questions completely
        if (prostateScreening) {
            prostateScreening.style.display = (gender === 'M' && age > 40) ? 'block' : 'none';
        }

        if (cervicalScreening) {
            cervicalScreening.style.display = (gender === 'F') ? 'block' : 'none';
        }

        if (breastScreening) {
            breastScreening.style.display = (gender === 'F') ? 'block' : 'none';
        }
    }

    updateScreeningVisibility();

    if (genderField) {
        genderField.addEventListener('change', updateScreeningVisibility);
    }

    if (ageField) {
        ageField.addEventListener('input', updateScreeningVisibility);
    }
});