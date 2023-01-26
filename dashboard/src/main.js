"use strict";

$(function() {
	// sets a function that will be called when the websocket connects/disconnects
	NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);
	
	// sets a function that will be called when the robot connects/disconnects
	NetworkTables.addRobotConnectionListener(onRobotConnection, true);
	
	// sets a function that will be called when any NetworkTables key/value changes
	NetworkTables.addGlobalListener(onValueChanged, true);
});

$(document).on('input', '.dub-slider', function() {
	NetworkTables.putValue($(this).data('key'), parseFloat($(this).val()));
});


function onRobotConnection(connected) {
	$('#robotstate').text(connected ? "Connected" : "Disconnected");
	$('#robotAddress').text(connected ? NetworkTables.getRobotAddress() : "Disconnected");

	updateColors();
	
}

function onNetworkTablesConnection(connected) {

	if (connected) {
		$("#connectstate").text("Connected");
		
		// clear the table
		$("#nt tbody > tr").remove();
		
	} else {
		$("#connectstate").text("Disconnected");
	}

	updateColors();

}

function onValueChanged(key, value, isNew) {

	// key thing here: we're using the various NetworkTable keys as
	// the id of the elements that we're appending, for simplicity. However,
	// the key names aren't always valid HTML identifiers, so we use
	// the NetworkTables.keyToId() function to convert them appropriately

	if (isNew) {
		var tr = $('<div class="table-info"></div>').appendTo($('#nt > .table'));
		$('<div class="table-label"></div>').text(key).appendTo(tr);
		$('<div class="table-area"></div>').attr('id', NetworkTables.keyToId(key))
					   .text(value)
					   .appendTo(tr);
	} else {
	
		// similarly, use keySelector to convert the key to a valid jQuery
		// selector. This should work for class names also, not just for ids
		$('#' + NetworkTables.keySelector(key)).text(value);
	}

	updateColors();

	$('.dub-slider').each(function() {
		$(this).val(NetworkTables.getValue($(this).data('key')));
	});

	$('.dub-text').each(function() {
		$(this).text(NetworkTables.getValue($(this).data('key')));
	});

}

function updateColors() {
	const ids = ['#connectstate', '#robotstate', '#robotAddress'];
	ids.forEach((v, _) => {
		if ($(v).text() == "Unknown") {
			$(v).css('background-color', '#cc241d');
		} else if ($(v).text() == "Disconnected") {
			$(v).css('background-color', '#cc241d');
		} else {
			$(v).css('background-color', '#689d6a');
		}
	});

	let pattern = /-dirty$/;
	if (pattern.test($("#git-hash-area").text())) {
		$("#git-hash-area").css('background-color', '#cc241d');
	} else {
		$("#git-hash-area").css('background-color', '#504945');
	}
}


// p5.js canvas


let img;

function preload() {
	img = loadImage(require('./assets/field.png'));
}

function setup() {
    let canvas = createCanvas(777, 377);
    canvas.parent("info-three");
	frameRate(24);
}

function draw() {
    background(220);
	image(img, 0, 0);
}

window.preload = preload;
window.setup = setup; 
window.draw = draw;
//window.keyPressed = keyPressed;