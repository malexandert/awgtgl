var map;
var geocoder;
var walkPath;
var arrMarkers=new Array(0);
var bounds;
var randcoords = [];

function mapToUrl(map) {
  var latlangstr = map.getCenter().toUrlValue();
}

function initialize() {
	geocoder = new google.maps.Geocoder();
	var myOptions = {
		zoom: 15,
		center: new google.maps.LatLng(40.4417384,-79.9545779),
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		mapTypeControlOptions: {
			style: google.maps.MapTypeControlStyle.DROPDOWN_MENU
		}
	};
	map = new google.maps.Map(document.getElementById("map"), myOptions);
}

function ftnButtonClicked() {
	if (arrMarkers) {
		for (i in arrMarkers) {
			arrMarkers[i].setMap(null);
		}
	}
	arrMarkers=new Array(0);
	var num=document.getElementById("nm").value;
	if (num<10) {
		plotrandom(num);
	}
}

function codeZip() {
    var address = document.getElementById("zip").value;
    geocoder.geocode( { 'address': address}, function(results, status) {
      if (status == google.maps.GeocoderStatus.OK) {
        map.setCenter(results[0].geometry.location);
        plotrandom(5);
      } else {
        alert("Geocode was not successful for the following reason: " + status);
      }
    });
}

function writeInJournal() {
	var text = document.getElementById("writer")
	var journal = document.getElementById("journal");

	var newEntry = document.createElement("li")
	newEntry.innerHTML = "\"" + text.value + "\""

	journal.insertBefore(newEntry, journal.firstChild);

	text.value =""

}

function plotrandom(number) {
	for (var i=0; i < arrMarkers.length; i++) {
		arrMarkers[i].setMap(null);
	}
	arrMarkers = [];
	if (walkPath != null) {
		walkPath.setMap(null);
	}
	bounds = map.getBounds();
	var southWest = bounds.getSouthWest();
	var northEast = bounds.getNorthEast();
	var lngSpan = northEast.lng() - southWest.lng();
	var latSpan = northEast.lat() - southWest.lat();
	pointsrand=[];

	for(var i=0; i<number; i++) {
    var randLat = southWest.lat() + latSpan * Math.random();
    var randLong = southWest.lng() + lngSpan * Math.random()
		var point = new google.maps.LatLng(randLat,randLong);
		pointsrand.push(point);
	}

	for(var i=0; i<number; i++) {
		var str_text=i+" : "+pointsrand[i];
		var marker=placeMarker(pointsrand[i],str_text);
		arrMarkers.push(marker);
		marker.setMap(map);
	}

  var encodedPath = google.maps.geometry.encoding.encodePath(pointsrand);
  console.log(encodedPath);

	walkPath = new google.maps.Polyline({
		path:pointsrand,
		strokeColor: "#0000FF",
		strokeOpacity: 0.9,
		strokeWeight: 2
	})

	walkPath.setMap(map)

}

function placeMarker(location,text) {
	var marker = new google.maps.Marker({
		position: location,
		map: map,
		title: text.toString(),
		draggable:false
	});
	return marker;
}

google.maps.event.addDomListener(window, 'load', initialize);
