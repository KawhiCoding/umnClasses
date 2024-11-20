function updateTable() {
    var table = document.getElementById("galleryTable");
    var now = new Date();

    for (var i = 1; i < table.rows.length; i++) {
        var saleDate = new Date(table.rows[i].cells[1].innerHTML);
        var timeDifference = saleDate.getTime() - now.getTime();
        if (timeDifference < 0) {
            table.rows[i].cells[2].innerHTML = "Auction Ended";
        } else {
            var seconds = Math.floor(timeDifference / 1000);
            var minutes = Math.floor(seconds / 60);
            var hours = Math.floor(minutes / 60);
            var days = Math.floor(hours / 24);
            table.rows[i].cells[2].innerHTML = days + " days " + hours % 24 + " hours " + minutes % 60 + " minutes " + seconds % 60 + " seconds";
        }
    }
}

const deleteButtons = document.querySelectorAll(".delete-btn");

deleteButtons.forEach(button => {
    button.addEventListener("click", function() {
        // Get the listing ID from the data attribute
        var listingId = button.getAttribute("data-listing-id");
        
        // Prepare the data to send in the DELETE request
        var deleteData = { listing_id: listingId };

        fetch("/api/delete_listing", {
            method: "DELETE",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify(deleteData)
        })
        .then(response => {
            if (response.status === 204) {
                // Remove the listing row from the table
                var row = button.closest('tr');
                row.remove();
                updateTable();
            } else if (response.status === 400) {
                alert("Listing not found.");
            } else {
                alert("An error occurred didnt delete listing.");
            }
        })
        .catch(error => {
            console.error("Error deleting listing:", error);
            alert("Network error. Please try again later.");
        });
    });
});
