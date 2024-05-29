function displaySelectedImage(input) {
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = function (e) {
        const imgElement = document.getElementById('selectedImage');
        imgElement.src = e.target.result;
      };
      reader.readAsDataURL(file);
    }
  }
  

  function submitForm(event) {
    event.preventDefault();  // Prevent the default form submission

    var formData = new FormData($('#yourFormId')[0]);

    $.ajax({
        type: 'POST',
        url: '/submit_form',
        data: formData,
        processData: false,
        contentType: false,
        success: function(response) {
            if (response.status === 'success') {
                // Display custom success message
                $('#resultMessage').text("Custom Success Message").addClass('success').show();
                
                // Optionally, you can clear the form fields or perform other actions
                $('#yourFormId')[0].reset();
            } else {
                // Display error message on the page
                $('#resultMessage').text(response.message).addClass('error').show();
            }
        },
        error: function(error) {
            console.log(error);
        }
    });
}

$(document).ready(function() {
  $("#addform").submit(function() {
      var countryCode = "+91";
      var phoneNumber = $("#phoneNumber").val();
      var fullPhoneNumber = countryCode + phoneNumber;
      $("#phoneNumber").val(fullPhoneNumber);
  });
});



