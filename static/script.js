document.addEventListener('DOMContentLoaded', () => {
    console.log("JS loaded"); // check this prints in browser dev console
    const arrow = document.querySelector('.arrow');

    window.addEventListener('scroll', () => {
        console.log("Scroll detected:", window.scrollY); // check this fires
        if (window.scrollY > 0) {
            arrow.classList.add('stop-bounce');
        } else {
            arrow.classList.remove('stop-bounce');
        }
    });
});
