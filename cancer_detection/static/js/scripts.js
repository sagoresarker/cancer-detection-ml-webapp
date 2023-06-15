/* static/js/script.js */
$(document).ready(function() {
    $('#imageForm').submit(function(e) {
        e.preventDefault();

        var formData = new FormData();
        formData.append('image', $('#imageInput')[0].files[0]);

        $.ajax({
            url: '{% url "detect_cancer" %}',
            type: 'POST',
            data: formData,
            processData: false,
            contentType: false,
            success: function(response) {
                var probability = response.cancer_probability;
                $('#result').text('Cancer Probability: ' + probability);
            },
            error: function(xhr, status, error) {
                $('#result').text('Error: ' + error);
            }
        });
    });
});
