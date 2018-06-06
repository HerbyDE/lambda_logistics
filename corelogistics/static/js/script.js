/**
 * Created by Herbert on 10/4/16.
 */

var map

function initMap() {
    map = new google.maps.Map(document.getElementById('map'), {
        center: {lat: -33.9465292, lng: 18.774546},
        zoom: 12
    });
}