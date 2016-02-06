// updateWiki updates #wiki-accordion with wiki search articles
var updateWiki = function(city) {

    // update screen using resource
    var updateWikiScreen = function(response) {
	if (response[1].length != 0) {	 
	    $('#wiki-accordion').empty();
	    for (i = 0; i < response[1].length; i++) {
		// parse response
		var title = response[1][i];
		var contents = response[2][i] + '<a href="' + 
		    response[3][i] + '" target="_blank"> [details]</a>';
		var collapse = (i < 2) ? " in" : ""; // open first two tabs
		$('#wiki-accordion').append('<div class="panel panel-primary">' +
					    '<div class="panel-heading">' +
					    '<h4 class="panel-title">' +
					    '<a data-toggle="collapse" data-parent="#accordion"' + 
					    'href="#collapse-wiki' + i + '">' +
					    title + '</a></h4></div>' +
					    '<div id="collapse-wiki' + i + 
					    '" class="panel-collapse collapse' + collapse  + '">' +
					    '<div class="panel-body"><p>' +
					    contents + '</p></div></div></div>');
	    }
	}
	else {
	    $('#wiki-accordion').empty();
	    $('#wiki-accordion').append('<div class="panel panel-warning">' +
					'<div class="panel-heading">' +
					'<h4 class="panel-title">' +
					'No Wiki articles - invalid input</h4></div></div>');
	}
    };

    // request resource
    $.ajax({
	url: "wiki-json/" + city,
	dataType: "json",
	success: function(response) {
	    updateWikiScreen(response['wiki-json']);
	}
    }).fail(function(e) {
	$('#wiki-accordion').empty();
	$('#wiki-accordion').append('<div class="panel panel-warning">' +
					'<div class="panel-heading">' +
					'<h4 class="panel-title">' +
					'No connection to Wiki</h4></div></div>');
    });
}; // END updateWiki
// -------------------------------------------------------------------------------------------------



// updateNYT updates #nyt-accordion with wiki search articles
var updateNYT = function(city) {

    // update screen using resource
    var updateNYTScreen = function(response) {
	//console.log(response['response']['docs']);
	
	if (response['response']['docs'].length != 0) {	 
	    $('#nyt-accordion').empty();
	    for (i = 0; i < response['response']['docs'].length; i++) {
		var article = response['response']['docs'][i]
		var title = article['headline']['main'];
		var contents = article['snippet'] + '<a href="' + 
		    article['web_url'] + '" target="_blank"> [details]</a>';
		var collapse = (i < 2) ? " in" : ""; // open first two tabs
		$('#nyt-accordion').append('<div class="panel panel-primary">' +
					    '<div class="panel-heading">' +
					    '<h4 class="panel-title">' +
					    '<a data-toggle="collapse" data-parent="#accordion"' + 
					    'href="#collapse-nyt' + i + '">' +
					    title + '</a></h4></div>' +
					    '<div id="collapse-nyt' + i + 
					    '" class="panel-collapse collapse' + collapse  + '">' +
					    '<div class="panel-body"><p>' +
					    contents + '</p></div></div></div>');
	    }
	}
	else {
	    $('#nyt-accordion').empty();
	    $('#nyt-accordion').append('<div class="panel panel-warning">' +
					'<div class="panel-heading">' +
					'<h4 class="panel-title">' +
					'No NYT articles - invalid input</h4></div></div>');
	}
	
    };

    // request resource
    $.ajax({
	url: "nyt-json/" + city,
	dataType: "json",
	success: function(response) {
	    updateNYTScreen(response['nyt-json']);
	}
    }).fail(function(e) {
	$('#nyt-accordion').empty();
	$('#nyt-accordion').append('<div class="panel panel-warning">' +
					'<div class="panel-heading">' +
					'<h4 class="panel-title">' +
					'No connection to NYT</h4></div></div>');
    });
}; // END updateWiki


// -------------------------------------------------------------------------------------------------



// runs if user input is valid to update screen components
var updateScreen = function(address) {
    var city = address[0];
    $('#city-input').val(city);
    updateWiki(city);
    updateNYT(city);
    // Replace with Google maps
    $('#google-img').attr('src', 'http://maps.googleapis.com/maps/api/streetview?' + 
	'size=600x400&location=' + city);
    /*
    $('#google-img').remove();
    $('#now-col').append('<img id="google-img" src="' +
			 'http://maps.googleapis.com/maps/api/streetview?size=600x400&location=' + 
			 city + '">');
    */
};

// run if user input is invalid
var pageFail = function() {
    $('#city-input').val("INVALID INPUT");
};

// TO DO ------------- country
// validate userInput using Google Maps
var validateCity = function(userInput) {
    $.ajax({
	url: "gmaps-json/" + userInput,
	dataType: "json",
	async: "false",
	success: function(response) {
	    if (response['gmaps-json']['status'] != 'ZERO_RESULTS') {
		var addressComp = response['gmaps-json']['results'][0]['address_components'];
		if (addressComp[0]['types'][0] == 'locality' && 
		    addressComp[0]['types'][1] == 'political') {
		    var longName = addressComp[0]['long_name'];
		    // country
		    updateScreen([longName]);
		}
		else {
		    pageFail();
		}}
	    else {
		pageFail();
	    }
	}
    })
}; // END validateCity


// run on load of site
$(function() {    
    $('#search-button').on('click', function() {
	var userInput = $('#city-input').val().toUpperCase();

	// validate user input
	validateCity(userInput);
    });
});
