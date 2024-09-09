// JavaScript to toggle the menu on mobile screens
document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.querySelector('.nav-toggle');
    const navLinks = document.querySelector('.nav-links');

    toggleButton.addEventListener('click', function () {
        navLinks.classList.toggle('active');
    });
});
