$(document).ready(function () {
    var rating_value = 0;

    $('#add_review').click(function () {
        $('#myModal').modal('show');
    });

    $(document).on('mouseenter', '.submit_star', function () {
        rating_value = $(this).data('rating');
        resetStar();
        for (var i = 1; i <= rating_value; i++) {
            $('#submit_star_' + i).addClass('text-warning');
        }
    });

    function resetStar() {
        for (var i = 0; i <= 5; i++) {
            $('#submit_star_' + i).addClass('star-light').removeClass('text-warning');
        }
    }

    $(document).on('click', '.submit_star', function () {
        rating_value = $(this).data('rating');
        resetStar();
        for (var i = 1; i <= rating_value; i++) {
            $('#submit_star_' + i).addClass('text-warning');
        }
    });

    $('#sendReview').click(function () {
        var userName = $('#userName').val();
        var userMessage = $('#userMessage').val();

        console.log('Rating Value:', rating_value);

        if (rating_value === undefined || rating_value === null) {
            alert('Please select a rating');
            return false;
        }

        if (userName.trim() === '' || userMessage.trim() === '') {
            alert('Please fill in both fields');
            return false;
        }

         $('#ratingInput').val(rating_value);
        $('#userNameInput').val(userName);
        $('#userMessageInput').val(userMessage);

         $('#reviewForm').submit();
        
    });


})

function fetchRatings() {
     const serverUrl = "/get_ratings";

     const room_id = window.location.pathname.split('/').pop();

    $.ajax({
        url: `${serverUrl}/get_ratings/${room_id}`,
        type: 'GET',
        success: function (response) {
             $('#avg_rating').text(response.average_rating.toFixed(1));
            $('#total_review').text(response.total_reviews);

             $('#total_five_star_review').text(response.five_star_reviews);
            $('#five_star_progress').css('width', response.five_star_percentage + '%');

            $('#total_four_star_review').text(response.four_star_reviews);
            $('#four_star_progress').css('width', response.four_star_percentage + '%');

            $('#total_three_star_review').text(response.three_star_reviews);
            $('#three_star_progress').css('width', response.three_star_percentage + '%');

            $('#total_two_star_review').text(response.two_star_reviews);
            $('#two_star_progress').css('width', response.two_star_percentage + '%');

            $('#total_one_star_review').text(response.one_star_reviews);
            $('#one_star_progress').css('width', response.one_star_percentage + '%');

             const displayReview = $('#display_review');
            displayReview.empty();  // Clear existing reviews

             response.reviews.forEach(function (review) {
                const reviewHtml = `<div class="review">
                                        <h5>${review.name}</h5>
                                        <p>${review.message}</p>
                                     </div>`;
                displayReview.append(reviewHtml);
            });
        },
        error: function (error) {
            console.error('Error fetching ratings:', error);
        }
    });
}

 $(document).ready(function () {
    fetchRatings();
});


 
document.addEventListener('DOMContentLoaded', function () {
     document.getElementById('reviewForm').addEventListener('submit', function (event) {
        event.preventDefault();  

         var formData = new FormData(this);

         fetch("/submit_review/" + room_id, {
            method: 'POST',
            body: formData
        })
        .then(response => response.json())
        .then(data => {
             if (data.success) {
                 showPopupAlert(data.message);
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });

     function showPopupAlert(message) {
        // Create popup alert element
        var popupAlert = document.createElement('div');
        popupAlert.classList.add('popup-alert');
        popupAlert.innerHTML = `
            <span class="popup-closebtn" onclick="closePopupAlert()">&times;</span>
            <b>${message}</b>
        `;
        
        // Append the popup alert to the body
        document.body.appendChild(popupAlert);

        // Automatically close the popup after 5 seconds
        setTimeout(function() {
            closePopupAlert();
        }, 5000);
    }

    // Function to close the popup alert
    function closePopupAlert() {
        var popupAlert = document.querySelector('.popup-alert');
        if (popupAlert) {
            popupAlert.style.display = 'none';
            // Optionally, remove the popup alert element from the DOM
            document.body.removeChild(popupAlert);
        }
    }
});
