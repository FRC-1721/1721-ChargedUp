"use strict";

import { countDownAlerts } from "./audioAlerts";


$(function () {
	// sets a function that will be called when the websocket connects/disconnects
	NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);

	// sets a function that will be called when the robot connects/disconnects
	NetworkTables.addRobotConnectionListener(onRobotConnection, true);

	// sets a function that will be called when any NetworkTables key/value changes
	NetworkTables.addGlobalListener(onValueChanged, true);
});

$(document).on('input', '.dub-slider', function () {
	NetworkTables.putValue($(this).data('key'), parseFloat($(this).val()));
});

$(document).on('click', '#aut-sel > button', function() {
	NetworkTables.putValue('/SmartDashboard/Autonomous/active', $(this).html());
});

$("#p-sw").change(function () {
	if (this.checked) {
		$("*").addClass('pink');
		$("#p-sw-l").removeClass('pink');
		$("#p-sw-s").removeClass('pink');
		$('#p-sw-l').css('background', '#c3768b');
		$('#p-sw-s').css('background', '#b3667b');
	} else {
		$("*").removeClass('pink');
		$('#p-sw-l').css('background', '');
		$('#p-sw-s').css('background', '');
	}
})

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

	$('.dub-slider').each(function () {
		$(this).val(NetworkTables.getValue($(this).data('key')));
	});

	$('.dub-text').each(function () {
		$(this).text(NetworkTables.getValue($(this).data('key')));
	});

	if (key.includes("/SmartDashboard/Audio")) {
		countDownAlerts(key, value);
	}

	if (key == "/SmartDashboard/Autonomous/options") {
		var options = NetworkTables.getValue("/SmartDashboard/Autonomous/options");
		$('#aut-sel').empty();
		options.forEach((v, i) => {
			$('<button></button>').attr('for', 'opt' + i)
				.html(v)
				.appendTo($('#aut-sel'));
		});
	}

	$("#aut-sel > button").each(function () {
		if ($(this).html() == NetworkTables.getValue("/SmartDashboard/Autonomous/active")) {
			$(this).css("background", "#802");
		} else {
			$(this).css("background", "#3c3836");
		}
	});

	if (key.includes("/SmartDashboard/Pose/Pose")) {
		updateRobotPos(NetworkTables.getValue(key), key.substr(key.length - 1));
	}
}

function highlightColor(patt, loc, css, overwrite = true, norm = '#504945') {
	if (patt.test($(loc).text())) {
		$(loc).css('background', css);
	} else if (overwrite) {
		$(loc).css('background', norm);
	}
}

function updateColors() {
	const ids = ['#connectstate', '#robotstate', '#robotAddress'];
	ids.forEach((v, _) => {
		if ($(v).text() == "Unknown") {
			$(v).css('background', 'linear-gradient(to right, #504945, #cc241d)');
		} else if ($(v).text() == "Disconnected") {
			$(v).css('background', 'linear-gradient(to right, #504945, #cc241d)');
		} else {
			$(v).css('background', 'linear-gradient(to right, #504945, #689d6a)');
		}
	});

	// Custom formatting
	highlightColor(/-dirty$/, "#git-hash-area", 'linear-gradient(to right, #504945, #cc241d)');

	// Programmers
	highlightColor(/SimUser$/, "#builder-area", 'linear-gradient(to right, #504945, #d3869b)'); // First one is fine to overwrite.
	highlightColor(/joe/, "#builder-area", 'linear-gradient(to right, #504945, #831598)', false);
	highlightColor(/dylan/, "#builder-area", 'linear-gradient(to right, #504945, #fe8019)', false);
	highlightColor(/kredcool/, "#builder-area", 'linear-gradient(to right, #504945, #67ab24)', false);

	// Branches
	highlightColor(/event/, "#git-branch-area", 'linear-gradient(to right, #504945, #689d6a)');
	highlightColor(/sim/, "#git-branch-area", 'linear-gradient(to right, #504945, #cc241d)', false);
}


// p5.js canvas

function getRandomInt(min, max) {
	return Math.floor(Math.random() * (max - min + 1)) + min;
}

let img, joe, dvd;
let posX, posY, posT;

let bounceJoe = [Math.random() < 0.5, Math.random() < 0.5, getRandomInt(0, 753), getRandomInt(0, 341)];
let bounceDvd = [Math.random() < 0.5, Math.random() < 0.5, getRandomInt(0, 681), getRandomInt(0, 328)];
let running = true;

function preload() {
	// Images
	img = loadImage(require('./assets/field.png'));
	joe = loadImage(require('./assets/joe.png'));
	dvd = loadImage(require('./assets/dvd.png'));
}

function setup() {
	let canvas = createCanvas(777, 377);
	canvas.parent("info-field-canvas");
	frameRate(24);
}

function draw() {
	background(220);
	image(img, 0, 0);
	image(dvd, bounceDvd[2], bounceDvd[3]);
	image(joe, bounceJoe[2], bounceJoe[3]);

	if (posX == undefined) {
		posX = NetworkTables.getValue("/SmartDashboard/Pose/Pose x");
		posY = NetworkTables.getValue("/SmartDashboard/Pose/Pose y");
		posT = NetworkTables.getValue("/SmartDashboard/Pose/Pose t");
	}
	
	rectMode(CENTER);
	push();
	translate(posX * 0.46977025392987, 377 - (posY * 0.46977025392987));
	rotate(radians(180 + posT));
	rect(0, 0, 24, 34);
	pop();
	rectMode(CORNER);
	if (running) {
		bounceJoe[2] += bounceJoe[0] ? 3 : -3;
		bounceJoe[3] += bounceJoe[1] ? 3 : -3;
		bounceDvd[2] += bounceDvd[0] ? 4 : -4;
		bounceDvd[3] += bounceDvd[1] ? 4 : -4;
		rect(5, 5, 5, 20);
		rect(20, 5, 5, 20);
	} else {
		triangle(5, 5, 25, 15, 5, 25);
	}
	if (bounceJoe[2] < 0 || bounceJoe[2] > 753) {
		bounceJoe[0] = !bounceJoe[0];
	}
	if (bounceJoe[3] < 0 || bounceJoe[3] > 341) {
		bounceJoe[1] = !bounceJoe[1];
	}
	if (bounceDvd[2] < 0 || bounceDvd[2] > 681) {
		96
		bounceDvd[0] = !bounceDvd[0];
	}
	if (bounceDvd[3] < 0 || bounceDvd[3] > 328) {
		49
		bounceDvd[1] = !bounceDvd[1];
	}
}

function mousePressed() {
	if (5 < mouseX && mouseX < 25 && 5 < mouseY && mouseX < 25) {
		running = !running;
	}
}

function updateRobotPos(v, i) {
	window["pos" + i.toUpperCase()] = v;
}

window.preload = preload;
window.setup = setup;
window.draw = draw;
window.mousePressed = mousePressed;
//window.keyPressed = keyPressed;
