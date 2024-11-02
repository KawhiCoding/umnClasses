document.getElementById("category").addEventListener("change", function() {
    const otherCategoryContainer = document.getElementById("other-category-container");
    if (this.value === "other") {
      otherCategoryContainer.style.display = "block";
    } else {
      otherCategoryContainer.style.display = "none";
    }
  });