import { modifyUserLatitude, modifyUserLongitude } from '/static/global_variables.js';
import { defaultLatitude, defaultLongitude, userLatitude, userLongitude } from '/static/global_variables.js';

let clickedButton = "";

document.getElementById('get-forecast-location').addEventListener('click', onForecastButtonClick);
document.getElementById('get-summary-location').addEventListener('click', onSummaryButtonClick);

function handleGeolocationSuccess(position) {
    console.log("Location -> success:", position);
    const { latitude, longitude } = position.coords;
    console.log(`${latitude}, ${longitude}`)
    modifyUserLatitude(latitude);
    modifyUserLongitude(longitude);
}

function handleGeolocationError(error) {
    let errorMessage = "";
    switch (error.code) {
        case error.PERMISSION_DENIED:
            errorMessage = "User denied the request for Geolocation.";
            break;
        case error.POSITION_UNAVAILABLE:
            errorMessage = "Location information is unavailable.";
            break;
        case error.TIMEOUT:
            errorMessage = "The request to get user location timed out.";
            break;
        case error.UNKNOWN_ERROR:
            errorMessage = "An unknown error occurred.";
            break;
    }
    document.getElementById(`status-${clickedButton}`).innerText = errorMessage;
    console.error("Geolocation error:", error);
}

export function getForecast(latitude, longitude) {
    fetch(`/forecast?lat=${latitude}&long=${longitude}`)
        .then(response => response.text())
        .then(data => {
                //table extraction
                const parser = new DOMParser();
                const doc = parser.parseFromString(data, "text/html");
                //const iconTable = tables.querySelector("table:nth-of-type(1)");
                const forecastTable = doc.querySelector("table");

                //iconTable.classList.add("border-collapse", "w-full", "divi", "border-gray-300", "text-center", "mt-4");
                forecastTable.classList.add("border-collapese", "w-full", "text-center", "mt-4");
            
                const rows = forecastTable.querySelectorAll("tr");
                rows.forEach(row => {
                    row.classList.add("divide-x-2", "divide-gray-900", "border");
                });
                
                document.getElementById('forecast-container').innerHTML = `
                        
                        ${forecastTable.outerHTML}
                    `;
                if (clickedButton){
                    document.getElementById(`status-${clickedButton}`).innerText = "";
                    clickedButton = "";
                    //console.log(`forecast for ${latitude} and long:${longitude}`)
                }
        })
        .catch(error => {
            document.getElementById('status-forecast').innerText = "Error fetching forecast!";
            console.error(error);
        });
}

export function getSummary(latitude, longitude) {
    fetch(`/summary?lat=${latitude}&long=${longitude}`)
        .then(response => response.text())
        .then(data => {
            const parser = new DOMParser();
            const doc = parser.parseFromString(data, "text/html");
            const summaryTable = doc.querySelector("table");
            summaryTable.classList.add("border-collapse", "w-[90%]", "text-center", "mt-4", "mx-auto");
            
            const rows = summaryTable.querySelectorAll("tr");
            rows.forEach(row => {
                row.classList.add("divide-x-2", "divide-gray-900", "border");
            });
            
            document.getElementById('summary-container').innerHTML = summaryTable.outerHTML;
            if (clickedButton) {
                document.getElementById(`status-${clickedButton}`).innerText = "";
                clickedButton = "";
            }
        })
        .catch(error => {
            document.getElementById('status-summary').innerText = "Error fetching forecast!";
            console.error(error);
        });
}

export function getUserLocation() {
    return new Promise((resolve, reject) => {
        if (navigator.geolocation) {
            if (clickedButton) {
                document.getElementById(`status-${clickedButton}`).innerText = "Fetching location...";
            }

            navigator.geolocation.getCurrentPosition(
                (position) => {
                    resolve(handleGeolocationSuccess(position));
                },
                (error) => {
                    reject(handleGeolocationError(error));
                }
            );
        } else {
            reject(new Error("Geolocation is not supported by this browser."));
        }
    });
}


function onForecastButtonClick() {
    console.log("Forecast button pressed");
    clickedButton = "forecast";
    if (userLatitude == null || userLongitude == null) {
        console.log("Fetching forecast for default position");
        getForecast(defaultLatitude, defaultLongitude);
    } else {
        getForecast(userLatitude, userLongitude);
    }
}

function onSummaryButtonClick() {
    console.log("Summary button pressed");
    clickedButton = "summary";
    if (userLatitude == null || userLongitude == null) {
        console.log("Fetching summary for default position");
        getSummary(defaultLatitude, defaultLongitude);
    } else {
        getSummary(userLatitude, userLongitude);
    }
    
}

//dark mode script

const toggleButton = document.getElementById('darkModeButton');

// Check saved / system theme preference
if (localStorage.getItem('theme') == 'dark') {
    document.body.classList.add('dark');
}
const prefersDarkScheme = window.matchMedia("(prefers-color-scheme: dark)").matches;
if (prefersDarkScheme && !localStorage.getItem('theme')) {
    document.body.classList.add('dark');
}

// dark mode button
toggleButton.addEventListener('click', () => {
    console.log("Switching to dark mode")
    document.body.classList.toggle('dark');

    if (document.body.classList.contains('dark')) {
        localStorage.setItem('theme', 'dark');
    } else {
        localStorage.setItem('theme', 'light');
    }
});
