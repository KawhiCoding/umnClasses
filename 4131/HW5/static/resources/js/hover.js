document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll(".listing-row");
    const previewArea = document.getElementById("preview-image");

    if (!previewArea) {
        console.error("Preview area element not found");
        return;
    }
    rows.forEach(function(row) {
        row.addEventListener("mouseenter", function() {
            const imageUrl = row.getAttribute("data-image");
            if (!imageUrl) {
                console.error("Image URL not found for row", row);
                return;
            }
            previewArea.src = imageUrl;
        });
    });
});
