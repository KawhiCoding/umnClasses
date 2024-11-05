document.addEventListener("DOMContentLoaded", function() {
    function updateCountdowns() {
        const countdownElements = document.querySelectorAll("[id^=countdown-]");
        countdownElements.forEach(function(element) {
            const endDate = new Date(element.getAttribute("data-end-date"));
            const now = new Date();

            let timeDiff = endDate - now;

            if (timeDiff <= 0) {
                element.textContent = "Auction ended";
            } else {
                const days = Math.floor(timeDiff / (1000 * 60 * 60 * 24));
                timeDiff %= (1000 * 60 * 60 * 24);
                const hours = Math.floor(timeDiff / (1000 * 60 * 60));
                timeDiff %= (1000 * 60 * 60);
                const minutes = Math.floor(timeDiff / (1000 * 60));
                timeDiff %= (1000 * 60);
                const seconds = Math.floor(timeDiff / 1000);

                element.textContent = `${days}d, ${hours}h, ${minutes}m, ${seconds}s`;
            }
        });
    }

    setInterval(updateCountdowns, 1000);
});