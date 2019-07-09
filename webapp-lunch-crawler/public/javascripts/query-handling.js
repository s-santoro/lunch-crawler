// prevent default form action and fire button event
$('form').submit(e => {
    e.preventDefault();
    $('#lunchButton').trigger('click');
});

// event-listener for button
$('#lunchButton').on('click', () => {
    // get input and process it
    let query = $('#lunchInput').val();
    $('#lunchInput').val('');
    query = getCleanedQuery(query);
    // get location => fetch restaurants wit 
    if(query.length >= 3) {
        fetchAndCreateMap(query);
    }
});

const getCleanedQuery = (query) => {
    // same preprocessing steps like prod-pipeline
    query = query.replace(/[^éàèÉÀÈäöüÄÖÜa-zA-Z]+/g, ' ');  // remove special characters
    query = query.toLowerCase();
    query = query.replace(/ä/g, 'a');
    query = query.replace(/ö/g, 'o');
    query = query.replace(/ü/g, 'u');
    queryLen = query.length;
    for (x = 0; x <= queryLen; x++) {
        query = query.replace(/(\s+|^)[a-z](\s+|$)/, ' ');  // remove single characters
        queryLen = query.length;
    }
    query = query.replace(/\s+/g, ' ');                     // remove multispaces
    return query;
}

const fetchAndCreateMap = (query) => {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            (pos) => fetchRestaurants(pos, query),
            () => alert("Wir benötigen deinen Standort für eine Menü-Empfehlung.")
        );
    } else {
        alert("Geolocation wird nicht vom Browser unterstützt.");
    }
}

const fetchRestaurants = (pos, query) => {
    coords = [pos.coords.latitude, pos.coords.longitude];
    // fetch restaurants
    fetch(`http://localhost:3000/lunch?item=${query}&location=${coords}`)
        .then(res => res.ok ? res.json() : null)
        // build map with restaurants
        .then(json => {
            return restaurants = json.hits.hits.map(item => {
                rest = item._source;
                return {name: rest.name, homepage: rest.homepage, coords: [rest.lat, rest.lon], menuURL: rest.menuURL[0]};
            });
        })
        .then(restaurants => {
            // create map of markers
            populateMap(coords, restaurants);
        })
        .catch(err => console.log(err));
}