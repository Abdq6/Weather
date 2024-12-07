export let userLatitude = null;
export let userLongitude = null;
export const defaultLatitude = 50.065;
export const defaultLongitude = 19.945;

export function modifyUserLatitude(latitude) {
    userLatitude = latitude;
}
export function modifyUserLongitude(longitude) {
    userLongitude = longitude;
}
