function newBid() {
  const form = document.querySelector(".new-bid");
  const toggleButton = document.getElementById("bid-btn"); 
  const submitButton = document.querySelector("#new-bid-submit");

  form.style.display = "none";

  toggleButton.addEventListener("click", function() {
      if (form.style.display === "none" || form.style.display === "") {
          form.style.display = "block";
          toggleButton.textContent = "Cancel Bid";
      } else {
          form.style.display = "none";
          toggleButton.textContent = "Place Bid";
      }
  });

  submitButton.addEventListener("click", async function(event) {
      event.preventDefault();
      
      const listingId = form.querySelector("input[name='listing_id']").value;
      const bidderName = form.querySelector("#new-bid-name").value;
      const bidAmount = parseFloat(form.querySelector("#new-bid-amount").value);
      const comment = form.querySelector("#new-bid-comment").value;

      const bidData = { listing_id: listingId, bidder_name: bidderName, new_bid_amount: bidAmount, comment: comment };

      try {
          const response = await fetch("/api/place_bid", {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify(bidData)
          });
          console.log(response);
          if (response.status === 201) {
              const bids = await response.json();
              renderBids(bids);
              form.style.display = "none";
              toggleButton.textContent = "Place Bid";
          } else if (response.status === 400) {
              form.querySelector("#new-bid-amount").style.border = "2px solid red";
              alert("Bid is not higher than the current highest bid.");
          } else {
              alert("Server error. Please try again.");
          }
      } catch (error) {
          console.error("Error placing bid:", error);
          alert("Network error. Please try again later.");
      }
  });
}

function renderBids(bids) {
    const bidList = document.querySelector(".bid-box");
    bidList.innerHTML = "";  // Clear current bids
    
    bids.forEach(bid => {
        const bidItem = document.createElement("li");
        bidItem.classList.add("bid-item");
        
        const bidder = document.createElement("span");
        bidder.classList.add("bidder-name");
        bidder.textContent = bid.name;  // Use "name" for bidder's name
        
        const amount = document.createElement("span");
        amount.classList.add("bid-amount");
        amount.textContent = `$${bid.amount.toFixed(2)}`;
        
        const comment = document.createElement("p");
        comment.classList.add("bid-comment");
        comment.textContent = bid.comment;

        // Append all elements to bidItem and bidList
        bidItem.appendChild(bidder);
        bidItem.appendChild(amount);
        bidItem.appendChild(comment);
        bidList.appendChild(bidItem);
    });
}

// Event listener to initialize new bids
document.addEventListener("DOMContentLoaded", newBid);

