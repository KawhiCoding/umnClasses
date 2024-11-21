document.addEventListener('DOMContentLoaded', function() {
  document.getElementById('category').addEventListener('change', function() {
    const otherCategory = document.getElementById('other_category');
    if (this.value === 'Other') {
        otherCategory.style.display = 'block';
    } else {
        otherCategory.style.display = 'none';
    }
  });
});
