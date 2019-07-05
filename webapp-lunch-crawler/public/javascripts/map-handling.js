// // show map TODO: (set position of user as centre)
// let mymap = L.map('mapid', { zoomControl:false }).setView([46.805, 8.20],8);
// L.tileLayer('https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=pk.eyJ1IjoiZ2lhbmJydW5uZXIiLCJhIjoiY2puazFqbXV3MGFmNTNrbWgyNG5zcDFyZSJ9.87l6WgQ_tzccQJif8HcnVA', {
//     attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
//     maxZoom: 20,
//     id: 'mapbox.streets',
//     accessToken: 'pk.eyJ1IjoiZ2lhbmJydW5uZXIiLCJhIjoiY2puazFqbXV3MGFmNTNrbWgyNG5zcDFyZSJ9.87l6WgQ_tzccQJif8HcnVA'
// }).addTo(mymap);

// let markers;
// function createMarkers(dataInput){
//     markers = L.markerClusterGroup();
//     dataInput.forEach(element => {
//         // create marker for all found restaurants
//         let lat = element.lat;
//         let lon = element.lon;
//         if(lat!=undefined&&lon!=undefined){
//             let marker = L.marker([lat, lon]);
//             // creat popup for marker
            
//             marker.bindPopup(popupString);      // add popup to marker
//             markers.addLayer(marker);           // add marker to cluster
//         }
//     });
//     mymap.addLayer(markers);
// }