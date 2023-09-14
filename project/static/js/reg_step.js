// $(function(){
// 	$("#wizard").steps({
//         headerTag: "h2",
//         bodyTag: "section",
//         transitionEffect: "fade",
//         enableAllSteps: true,
//         transitionEffectSpeed: 500,
//         labels: {
//             finish: "Submit",
//             next: "Forward",
//             previous: "Backward"
//         }
//     });
//     $('.wizard > .steps li a').click(function(){
//     	$(this).parent().addClass('checked');
// 		$(this).parent().prevAll().addClass('checked');
// 		$(this).parent().nextAll().removeClass('checked');
//     });
//     // Custome Jquery Step Button
//     $('.forward').click(function(){
//     	$("#wizard").steps('next');
//     })
//     $('.backward').click(function(){
//         $("#wizard").steps('previous');
//     })
//     // Select Dropdown
//     $('html').click(function() {
//         $('.select .dropdown').hide(); 
//     });
//     $('.select').click(function(event){
//         event.stopPropagation();
//     });
//     $('.select .select-control').click(function(){
//         $(this).parent().next().toggle();
//     })    
//     $('.select .dropdown li').click(function(){
//         $(this).parent().toggle();
//         var text = $(this).attr('rel');
//         $(this).parent().prev().find('div').text(text);
//     })
// })

function handleSubmit(step) {
    // Serialize the form data for the current step
    var formData = $('#form-step' + step).serialize();

    // Get the CSRF token from the page
    var csrfToken = $('input[name=csrfmiddlewaretoken]').val();

    // Send an AJAX POST request to your Django view
    $.ajax({
        type: 'POST',
        url: '{% url "seller_reg_step" %}',
        data: formData,
        headers: {
            'X-CSRFToken': csrfToken  // Include the CSRF token in the request headers
        },
        success: function (response) {
            // Handle the response here if needed
            console.log(response);

            // Disable all previous tabs (you may need to adjust this part)
            for (var i = 1; i < step; i++) {
                $('#tab' + i).prop('disabled', true);
            }

            // Enable the next tab (if available)
            if (step < 4) {  // Adjust '4' to the total number of steps
                $('#tab' + (step + 1)).prop('disabled', false);

                // Switch to the next tab
                $('#tab' + (step + 1)).prop('checked', true);
            }
        },
        error: function (xhr, textStatus, errorThrown) {
            // Handle errors if needed
            console.error(xhr.responseText);
        }
    });
}

// Add event listeners to the "Save" buttons for each step
$(document).ready(function () {
    $('.form-submit').click(function (event) {
        event.preventDefault();  // Prevent the default form submission
        var step = $(this).data('step');
        handleSubmit(step);  // Call the form submission function with the step
    });
});







// document.addEventListener("DOMContentLoaded", function () {
//     const tabs = document.querySelectorAll('input[type="radio"]');
//     const saveButtons = document.querySelectorAll('.form-submit');
//     let currentTab = 0;

//     // Disable all tabs except the first one initially
//     for (let i = 1; i < tabs.length; i++) {
//         tabs[i].disabled = true;
//     }

//     // Add event listeners to the "Save" buttons
//     for (let i = 0; i < saveButtons.length; i++) {
//         saveButtons[i].addEventListener("click", function () {
//             // Check if the form is valid (you can add your form validation logic here)
//             const isFormValid = true; // Replace with your validation logic

//             if (isFormValid) {
//                 // Disable all previous tabs
//                 for (let i = 0; i < currentTab; i++) {
//                     tabs[i].disabled = true;
//                 }

//                 // Enable the next tab (if available)
//                 if (currentTab < tabs.length - 1) {
//                     tabs[currentTab + 1].disabled = false;

//                     // Switch to the next tab
//                     tabs[currentTab + 1].checked = true;

//                     // Update the current tab
//                     currentTab++;
//                 }
//             }
//         });
//     }
// });

