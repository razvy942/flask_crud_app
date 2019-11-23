const searchInput = document.querySelector('#search-input');
const searchButton = document.querySelector('#search-button');

// Get value from search field and redirect user to search url
searchButton.addEventListener('click', (e) => {
    e.preventDefault();
    searchTerm = searchInput.value;
    base_url = window.location.origin;
    window.location.href = `${base_url}/search/${searchTerm}`;
});

