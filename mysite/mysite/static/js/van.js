// Function to fade out messages smoothly
setTimeout(function() {
    document.querySelectorAll('.alert').forEach(function(alert) {
        alert.style.transition = 'opacity 0.5s ease'; // Add CSS transition
        alert.style.opacity = 0; // Set opacity to 0 for fade out effect
        setTimeout(function() {
            alert.style.display = 'none'; // Hide the message after fade out
        }, 500); // Wait for 0.5 seconds before hiding
    });
}, 1000); // Wait for 1 second before starting the fade out effect
