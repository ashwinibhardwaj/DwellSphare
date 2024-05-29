document.addEventListener("DOMContentLoaded", function () {
    let previewContainer = document.querySelector('.products-preview');
    let previewBox = previewContainer.querySelector('.preview');
 
    document.querySelectorAll('.products-container .product').forEach(product => {
       product.onclick = () => {
          let name = product.getAttribute('data-name');
          let preview = previewContainer.querySelector(`[data-target="${name}"]`);
 
          // Set the details in the popup based on the clicked product
          preview.querySelector('h3').textContent = "Name of the Hostel"; // You can replace this with the actual data
          // Set other details similarly...
 
          // Display the popup
          previewContainer.style.display = 'flex';
       };
    });
 
    previewBox.querySelector('.fa-times').onclick = () => {
       previewContainer.style.display = 'none';
    };
 });


 function openPreview() {
   window.location.href = '/preview';
}

document.addEventListener('DOMContentLoaded', function () {
   var messageButtons = document.querySelectorAll('.btn.message-owner');
   var popup = document.getElementById('message-popup');
   var overlay = document.getElementById('message-popup-overlay');
   var closeButton = document.getElementById('close-popup');
   var sendButton = document.getElementById('send-message');
   var messageInput = document.getElementById('message-input');
 
   function openPopup() {
     popup.style.display = 'block';
     overlay.style.display = 'block';
   }
 
   function closePopup() {
     popup.style.display = 'none';
     overlay.style.display = 'none';
   }
 
   messageButtons.forEach(function (button) {
     button.addEventListener('click', openPopup);
   });
 
   closeButton.addEventListener('click', closePopup);
 
   sendButton.addEventListener('click', function () {
     var message = messageInput.value;
     closePopup();
   });
 });

 fetch('/send_message', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    "room_id": yourRoomIdHere,
  }),
})
  .then(response => response.json())
  .then(data => console.log(data))
  .catch(error => console.error('Error:', error));

  setTimeout(function() {
    document.getElementById('alert').style.display = 'none';
}, 5000);

// Function to close the alert
function closeAlert() {
    document.getElementById('alert').style.display = 'none';
}