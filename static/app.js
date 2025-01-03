document.getElementById('search-btn').addEventListener('click', function() {
    let title = document.getElementById('movie-title').value;
    let genre = document.getElementById('movie-genre').value;

    fetch(`/search?title=${title}&genre=${genre}`)
        .then(response => response.json())
        .then(data => {
            let resultsDiv = document.getElementById('search-results');
            resultsDiv.innerHTML = '';  
            if (data.length > 0) {
                data.forEach(movie => {
                    let movieDiv = document.createElement('div');
                    movieDiv.innerHTML = `
                        <h3>${movie.title}</h3>
                        <p>Genre: ${movie.genre}</p>
                        <button class="recommend-btn" data-id="${movie.id}">Get Recommendations</button>
                    `;
                    resultsDiv.appendChild(movieDiv);
                });
            } else {
                resultsDiv.innerHTML = 'No movies found.';
            }
        });
});

document.getElementById('search-results').addEventListener('click', function(e) {
    if (e.target.classList.contains('recommend-btn')) {
        let movieId = e.target.getAttribute('data-id');
        fetch(`/recommendations/${movieId}`)
            .then(response => response.json())
            .then(data => {
                let recommendationsDiv = document.getElementById('recommendations');
                recommendationsDiv.innerHTML = '';  
                if (data.length > 0) {
                    data.forEach(movie => {
                        let recDiv = document.createElement('div');
                        recDiv.innerHTML = `
                            <h3>${movie.title}</h3>
                            <p>Genre: ${movie.genre}</p>
                        `;
                        recommendationsDiv.appendChild(recDiv);
                    });
                } else {
                    recommendationsDiv.innerHTML = 'No recommendations available.';
                }
            });
    }
});


