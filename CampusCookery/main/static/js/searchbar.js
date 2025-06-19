function toggleSearchType() {
  const toggleIcon = document.getElementById("searchTypeToggle")
  const typeInput = document.getElementById("searchTypeInput")

  // Ensure elements exist
  if (!toggleIcon || !typeInput) return

  // Switch search type on toggle icon click
  toggleIcon.addEventListener('click', function() {
    // Switch between recipes ands articles
    if (toggleIcon.classList.contains('fa-utensils')) {
      toggleIcon.classList.remove('fa-utensils');
      toggleIcon.classList.add('fa-book');
      toggleIcon.setAttribute("title", "Articles") // Mouseover for accesibility
      typeInput.value = 'articles'; // Set hidden input for forum
    } else {
      toggleIcon.classList.remove('fa-book');
      toggleIcon.classList.add('fa-utensils');
      toggleIcon.setAttribute("title", "Recipes")
      typeInput.value = 'recipes';
      }
  });
}

function toggleSearchModal() {
  const toggleIcon = document.getElementById("searchFilterToggle")
  const filterModal = document.getElementById("searchFilterModal")

  // Ensure elements exist
  if (!toggleIcon || !filterModal) return

  // Show filter modal on toggle icon click
  toggleIcon.addEventListener("click", () => {
    if (filterModal.classList.contains('hidden')) {
      filterModal.classList.remove('hidden');
    } else {
      filterModal.classList.add('hidden');
    }
  })
}

function preserveSearchState() {
  const currentUrl = new URL(window.location.href);
  const params = new URLSearchParams(currentUrl.search);

  // Preserve toggle icon if search type is already set, otherwise defaults to utensils
  const currentType = params.get('type');

  const toggleIcon = document.getElementById("searchTypeToggle")
  const typeInput = document.getElementById("searchTypeInput")

  if (currentType == "articles") {
    toggleIcon.classList.remove('fa-utensils');
    toggleIcon.classList.add('fa-book');
    toggleIcon.setAttribute("title", "Articles");
    typeInput.value = 'articles';
  }

  // Preserve seleted tags in search filter modal
  const currentTags = params.getAll('tags');
  const tagCheckboxes = document.querySelectorAll('.search-tags label input');

  tagCheckboxes.forEach(checkbox => {
    if (currentTags.includes(checkbox.value)) {
      checkbox.checked = true;
    }
  })

  // Preserve search query in search bar
  const query = params.get('q');
  const searchInput = document.getElementById("searchInput");

  searchInput.value = query;
}

// Add event listeners
document.addEventListener("DOMContentLoaded", toggleSearchType())
document.addEventListener("DOMContentLoaded", toggleSearchModal())
document.addEventListener("DOMContentLoaded", preserveSearchState())
