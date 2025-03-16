document.addEventListener('DOMContentLoaded', function () {
    const dependencies = [
        { questionId: 'id_allergies', detailId: 'id_allergies_detail' },
        { questionId: 'id_chronic_disease_status', detailId: 'id_chronic_disease_detail' },
        { questionId: 'id_smoking_status', detailId: 'id_smoking_detail' },
        { questionId: 'id_alcohol_status', detailId: 'id_alcohol_detail' },
    ];

    function toggleFollowUp(questionId, detailId) {
        const question = document.getElementById(questionId);
        const detail = document.getElementById(detailId);

        if (!question || !detail) {
            console.warn(`Missing element: ${!question ? questionId : detailId}`);
            return;
        }

        // Optional: Hide both the label and the input
        const label = document.querySelector(`label[for="${detailId}"]`);

        if (question.value === 'Yes') {
            detail.style.display = 'block';
            if (label) label.style.display = 'block';
        } else {
            detail.style.display = 'none';
            if (label) label.style.display = 'none';
        }
    }

    dependencies.forEach(({ questionId, detailId }) => {
        const question = document.getElementById(questionId);
        if (question) {
            question.addEventListener('change', () => toggleFollowUp(questionId, detailId));
            toggleFollowUp(questionId, detailId); // On page load
        }
    });
});

// document.addEventListener('DOMContentLoaded', function() {
//     const container = document.getElementById('onboarding-container');
//     const age = parseInt(container.dataset.userAge, 10);
//     const gender = container.dataset.userGender.toLowerCase();

//     // Question wrappers (wrap each target question in a <p> or <div> with these IDs)
//     const prostateQuestion = document.querySelector('id_prostate_screening');
//     const cervicalQuestion = document.getElementById('id_cervical_cancer_screening');
//     const breastQuestion = document.getElementById('id_breast_cancer_screening');

//     if (prostateQuestion) prostateQuestion.style.display = 'none';
//     if (cervicalQuestion) cervicalQuestion.style.display = 'none';
//     if (breastQuestion) breastQuestion.style.display = 'none';

//     if (gender === 'Male' && age >= 40 && prostateQuestion) {
//         prostateQuestion.style.display = 'block';
//     }

//     if (gender === 'Female' && age >= 18) {
//         if (cervicalQuestion) cervicalQuestion.style.display = 'block';
//         if (breastQuestion) breastQuestion.style.display = 'block';
//     }
// });