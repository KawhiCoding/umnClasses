document.addEventListener('DOMContentLoaded', function () {
    const rows = document.querySelectorAll('.galleryTable tbody tr');
    const previewImage = document.getElementById('preview-image');
    const previewDescription = document.getElementById('preview-description');

    rows.forEach(row => {
        row.addEventListener('mouseenter', function () {
            const imageSrc = this.getAttribute('data_image');
            const description = this.getAttribute('data_description');

            previewImage.src = imageSrc;
            previewImage.style.display = 'block';
            previewDescription.textContent = description;
        });

        row.addEventListener('mouseleave', function () {
            // Optionally clear the preview when leaving the row
            // previewImage.style.display = 'none';
            // previewDescription.textContent = '';
        });
    });
});
