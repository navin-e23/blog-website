// Simple auto-scroll for the featured slider on homepage
document.addEventListener('DOMContentLoaded', function () {
    const track = document.querySelector('.slider-track');
    if (!track) return;

    let scrollAmount = 0;
    setInterval(() => {
        scrollAmount += 260;
        if (scrollAmount >= track.scrollWidth) {
            scrollAmount = 0;
        }
        track.scrollTo({ left: scrollAmount, behavior: 'smooth' });
    }, 3000);
});
