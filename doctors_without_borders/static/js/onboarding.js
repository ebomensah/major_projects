document.addEventListener('DOMContentLoaded', function() {
    // Function to show or hide follow-up question based on the selected value
    function toggleFollowUp(questionId, detailsId) {
        const question = document.getElementById(questionId);
        const details = document.getElementById(detailsId);

        // Check if question exists and has the correct answer
        if (question && details) {
            if (question.value === 'yes') {
                details.style.display = 'block'; // Show the details if answer is "Yes"
            } else {
                details.style.display = 'none'; // Hide the details if answer is "No"
            }
        }
    }

    // Set up event listeners for each question (status questions)
    const allergiesQuestion = document.getElementById('allergies');
    if (allergiesQuestion) {
        allergiesQuestion.addEventListener('change', function() {
            toggleFollowUp('allergies', 'allergies-details');
        });
    }

    const chronicDiseaseQuestion = document.getElementById('chronic_disease');
    if (chronicDiseaseQuestion) {
        chronicDiseaseQuestion.addEventListener('change', function() {
            toggleFollowUp('chronic_disease', 'chronic-disease-details');
        });
    }

    const smokeQuestion = document.getElementById('smoke');
    if (smokeQuestion) {
        smokeQuestion.addEventListener('change', function() {
            toggleFollowUp('smoke', 'smoke-details');
        });
    }

    const alcoholQuestion = document.getElementById('alcohol');
    if (alcoholQuestion) {
        alcoholQuestion.addEventListener('change', function() {
            toggleFollowUp('alcohol', 'alcohol-details');
        });
    }

    // Initial check to make sure any previously selected options are respected
    toggleFollowUp('allergies', 'allergies-details');
    toggleFollowUp('chronic_disease', 'chronic-disease-details');
    toggleFollowUp('smoke', 'smoke-details');
    toggleFollowUp('alcohol', 'alcohol-details');
});