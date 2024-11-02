document.addEventListener("DOMContentLoaded", function() {
  const form = document.getElementById("bidForm");
  const toggleButton = document.getElementById("toggleBidFormBtn");

  form.addEventListener("click", function() {
    if (form.style.display === "none" || form.style.display === "") {
        form.style.display = "block";
        toggleButton.textContent = "Cancel Bid";
    } else {
        form.style.display = "none";
        toggleButton.textContent = "Place Bid";
    }
  });
});