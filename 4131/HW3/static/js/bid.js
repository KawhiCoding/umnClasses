function newBid() {
  const form = document.getElementsByClassName("new-bid")[0];
  const toggleButton = document.getElementById("bid-btn"); 

  // Ensure the form is initially hidden
  

  toggleButton.addEventListener("click", function() {
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block"; 
        toggleButton.textContent = "Cancel Bid"; 
    } else {
        form.style.display = "none"; 
        toggleButton.textContent = "Place Bid";
    }
  });
}

document.addEventListener("DOMContentLoaded", newBid);