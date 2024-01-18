// Your existing code...

// Get all the stars
const stars = document.querySelectorAll('.star');

// Function to handle highlighting stars on hover
const handleStarHover = (size) => {
    stars.forEach((star, index) => {
        if (index < size) {
            star.classList.add('hovered');
        } else {
            star.classList.remove('hovered');
        }
    });
};

// Event listeners for mouseover and click on each star
stars.forEach((star, index) => {
    star.addEventListener('mouseover', () => {
        handleStarHover(index + 1);
    });

    star.addEventListener('click', () => {
        handleSelect(star.id);
    });
});

// Your existing code...
