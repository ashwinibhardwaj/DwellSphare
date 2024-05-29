document.addEventListener("DOMContentLoaded", function () {
  document.querySelector('.jsFilter').addEventListener('click', function () {
    document.querySelector('.filter-menu').classList.toggle('active');
  });

  document.querySelector('.grid').addEventListener('click', function () {
    document.querySelector('.list').classList.remove('active');
    document.querySelector('.grid').classList.add('active');
    document.querySelector('.products-area-wrapper').classList.add('gridView');
    document
      .querySelector('.products-area-wrapper')
      .classList.remove('tableView');
  });

  document.querySelector('.list').addEventListener('click', function () {
    document.querySelector('.list').classList.add('active');
    document.querySelector('.grid').classList.remove('active');
    document.querySelector('.products-area-wrapper').classList.remove('gridView');
    document.querySelector('.products-area-wrapper').classList.add('tableView');
  });

  var modeSwitch = document.querySelector('.mode-switch');
  modeSwitch.addEventListener('click', function () {
    document.documentElement.classList.toggle('light');
    modeSwitch.classList.toggle('active');
  });

  document.addEventListener("DOMContentLoaded", function () {
    // Get the current page URL
    var currentPage = window.location.pathname.split('/').pop();

    // Get all sidebar list items
    var sidebarItems = document.querySelectorAll('.sidebar-list-item');

    // Loop through sidebar items to find the active one
    sidebarItems.forEach(function (item) {
      var link = item.querySelector('a');
      var href = link.getAttribute('href');

      // Check if the current page URL matches the sidebar item's href
      if (currentPage === href) {
        item.classList.add('active');
      }
    });
  });

  document.getElementById('addproperty').addEventListener('click', function () {
    // Call a function to execute the Python file on button click
    executePythonFile();
  });

  function executePythonFile() {
    // Use AJAX or fetch to make a request to the backend
    fetch('/run-python-file')
      .then(response => response.json())
      .then(data => {
        console.log(data); // Log the response from the server
      })
      .catch(error => console.error(error));
  }

  document.getElementById('addproperty').addEventListener('click', function () {
    // Call a function to run the Python script on button click
    runAddPropertyScript();
  });

  function runAddPropertyScript() {
    // Use AJAX to send a request to the Flask server (add_property_form)
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "http://127.0.0.1:5001/run-add-property-script", true);
    xhr.onreadystatechange = function () {
      if (xhr.readyState == 4 && xhr.status == 200) {
        console.log("Python script executed successfully");
      }
    };
    xhr.send();
  }
});




$(document).ready(function() {
  // Function to check if the profile exists
  function checkProfile() {
      $.ajax({
          type: 'GET',
          url: '/check_profile',  // Endpoint to check if the profile exists
          success: function(response) {
              if (response.exists) {
                  // Profile exists, show a message for 2 seconds
                  $('#profile-message').text('Profile already filled.').fadeIn(2000, function() {
                      $(this).fadeOut();
                  });
              } else {
                  // Profile doesn't exist, show the fill profile form
                  $('#fill-profile-form').show();
              }
          },
          error: function(error) {
              console.error('Error checking profile:', error);
          }
      });
  }

  // Call the checkProfile function on page load
  checkProfile();

  // Bind the checkProfile function to the fill profile button click event
  $('#fill-profile-button').click(function() {
      checkProfile();
  });
});