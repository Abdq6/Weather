import { getUserLocation, getForecast, getSummary } from '/static/script.js';
import { modifyUserLatitude, modifyUserLongitude } from '/static/global_variables.js';
import { userLatitude, userLongitude, defaultLatitude, defaultLongitude } from '/static/global_variables.js';

let currentPosition = null;

getUserLocation()
    .then(() => {
        initializeMap(userLatitude, userLongitude);
        getForecast(userLatitude, userLongitude);
        getSummary(userLatitude, userLongitude);
    })
    .catch((error) => {
        console.error("Couldn't retrieve initial location:", error);
        initializeMap(defaultLatitude, defaultLongitude);
    });

function initializeMap(latitude, longitude) {
    const map = L.map('map').setView([latitude, longitude], 13);

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; OpenStreetMap contributors'
    }).addTo(map);

    currentPosition = L.marker([latitude, longitude]).addTo(map)
        .bindPopup('This is where you are!')
        .openPopup();

    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const long = e.latlng.lng;

        modifyUserLatitude(lat);
        modifyUserLongitude(long);
        
        if (currentPosition) {
            currentPosition.remove();
        }

        currentPosition = L.marker([lat, long]).addTo(map)
            .bindPopup(`Clicked location: ${lat.toFixed(4)}, ${long.toFixed(4)}`)
            .openPopup();
    });
}
