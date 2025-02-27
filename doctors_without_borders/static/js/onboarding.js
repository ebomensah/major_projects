document.addEventListener("DOMContentLoaded", function() {
    console.log("🚀 JavaScript Loaded!");

    function toggleField(choiceFieldId, targetFieldId) {
        let choiceField = document.getElementById(choiceFieldId);
        let targetField = document.getElementById(targetFieldId);

        if (choiceField && targetField) {
            function updateVisibility() {
                targetField.style.display = (choiceField.value === 'Yes') ? 'block' : 'none';
            }

            choiceField.addEventListener('change', updateVisibility);
            updateVisibility(); 
        }
    }

    toggleField('id_allergies', 'id_allergies_detail');
    toggleField('id_chronic_disease_status', 'id_chronic_disease_detail');
    toggleField('id_smoking_status', 'id_smoking_detail');
    toggleField('id_alcohol_status', 'id_alcohol_detail');

    // ✅ Fetch gender & age from userData
    const gender = userData.gender;
    const age = userData.age;

    console.log("🟢 Gender:", gender);
    console.log("🟢 Age:", age);

    // Screenings
    const prostateScreening = document.getElementById('prostate-screening');
    const cervicalScreening = document.getElementById('cervical-cancer-screening');
    const breastScreening = document.getElementById('breast-cancer-screening');

    console.log("🔍 Checking Screening Elements:", {
        prostateScreening,
        cervicalScreening,
        breastScreening
    });

    // 🚨 Check if elements exist before modifying them
    if (prostateScreening) {
        prostateScreening.style.display = (gender === 'M' && age > 40) ? 'block' : 'none';
    } else {
        console.warn("⚠️ prostate-screening element not found!");
    }

    if (cervicalScreening) {
        cervicalScreening.style.display = (gender === 'F') ? 'block' : 'none';
    } else {
        console.warn("⚠️ cervical-cancer-screening element not found!");
    }

    if (breastScreening) {
        breastScreening.style.display = (gender === 'F') ? 'block' : 'none';
    } else {
        console.warn("⚠️ breast-cancer-screening element not found!");
    }
});