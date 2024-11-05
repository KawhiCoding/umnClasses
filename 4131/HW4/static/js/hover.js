document.addEventListener("DOMContentLoaded", function() {
    const rows = document.querySelectorAll(".listing-row");
    const previewArea = document.getElementById("preview-image");

    rows.forEach(function(row) {
        row.addEventListener("mouseenter", function() {
            const imageUrl = row.getAttribute("data-image");

            previewArea.innerHTML = `
                <h3>Auction Preview</h3>
                <img src="${imageUrl}" alt="Auction Image" style="max-width: 100%;">
            `;
        });
    });
});