let markers = null;
let mymap = null;
let user = null;

const populateMap = (coords, restaurants) => {
    // initialize map once
    if (mymap === null) {
        mymap = L.map('mapid', { zoomControl: false }).setView(coords, 12);
        L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ2lhbmJydW5uZXIiLCJhIjoiY2puazFqbXV3MGFmNTNrbWgyNG5zcDFyZSJ9.87l6WgQ_tzccQJif8HcnVA', {
            attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
            maxZoom: 20,
            id: 'mapbox.streets',
            accessToken: 'pk.eyJ1IjoiZ2lhbmJydW5uZXIiLCJhIjoiY2puazFqbXV3MGFmNTNrbWgyNG5zcDFyZSJ9.87l6WgQ_tzccQJif8HcnVA'
        }).addTo(mymap);
    }
    else {
        mymap.setView(coords);
    }

    // place location of user
    if (user === null) {
        let icon = L.icon({
            iconUrl: './images/user.png',
            iconSize: [38, 38],
            iconAnchor: [19, 38],
            popupAnchor: [0, -31]
        });
        user = L.marker(coords, { icon: icon });
        let popup = "<p>Mein Standort</p>"
        user.bindPopup(popup);
        mymap.addLayer(user);
    }
    // coords of user changed
    if (coords[0] != user.lat || coords[1] != user.lon) {
        user.setLatLng(coords);
    }

    if (markers != null) {
        mymap.removeLayer(markers);
    }
    markers = L.markerClusterGroup();
    restaurants.forEach(element => {
        // create marker for all found restaurants
        let lat = element.coords[0];
        let lon = element.coords[1];
        if (lat != undefined && lon != undefined) {
            let icon = L.icon({
                iconUrl: './images/pin.svg',
                iconSize: [38, 38],
                iconAnchor: [19, 38],
                popupAnchor: [0, -31]
            });
            let marker = L.marker([lat, lon], { icon: icon });
            // creat popup for marker
            let popup = L.popup()
                .setContent(
                    `<div><p><b>${element.name}</b></p>` +
                    `<p><a href="http://www.${element.homepage}">Startseite</a></p>` +
                    `<p><a href="${element.menuURL}">Menüseite</a></p></div>`
                );
            let popOptions = {
                'className': 'popup'
            };
            marker.bindPopup(popup, popOptions);      // add popup to marker
            markers.addLayer(marker);           // add marker to cluster
        }
    });
    mymap.addLayer(markers);
}
