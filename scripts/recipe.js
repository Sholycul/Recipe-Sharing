document.addEventListener('DOMContentLoaded', function() {
    function initSlider(sliderId) {
        const slider = document.getElementById(sliderId);
        const images = slider.getElementsByTagName('img');
        let currentIndex = 0;

        function showImage(index) {
            for (let i = 0; i < images.length; i++) {
                images[i].classList.remove('active');
            }
            images[index].classList.add('active');
        }

        function nextImage() {
            currentIndex = (currentIndex + 1) % images.length;
            showImage(currentIndex);
        }

        showImage(currentIndex);
        setInterval(nextImage, 3000); // Change image every 3 seconds
    }

    initSlider('explore-slider');
    initSlider('share-slider');
});