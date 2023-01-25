"use strict";

$(function () {
	// sets a function that will be called when the websocket connects/disconnects
	NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);

	// sets a function that will be called when the robot connects/disconnects
	NetworkTables.addRobotConnectionListener(onRobotConnection, true);

	// sets a function that will be called when any NetworkTables key/value changes
	NetworkTables.addGlobalListener(onValueChanged, true);
});


function onRobotConnection(connected) {
	$('#robotstate').text(connected ? "Connected" : "Disconnected");
	$('#robotAddress').text(connected ? NetworkTables.getRobotAddress() : "Disconnected");

	updateColors();

}

function ntLoaded() {
	NetworkTables.addGlobalListener(function (key, value, isNew) {
		// do something with the values as they change
	}, true);

	NetworkTables.putValue('/networktablesLoaded', true);
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


	console.log("here");

	$('#ntmtst').text(NetworkTables.getValue('/SmartDashboard/Test/test', 0));

	$('#build-date-area').text(NetworkTables.getValue('/SmartDashboard/BuildData/deploy-date', 0));
	$('#build-host-area').text(NetworkTables.getValue('/SmartDashboard/BuildData/deploy-host', 0));
	$('#builder-area').text(NetworkTables.getValue('/SmartDashboard/BuildData/deploy-user', 0));
	$('#git-branch-area').text(NetworkTables.getValue('/SmartDashboard/BuildData/git-branch', 0));
	$('#git-hash-area').text(NetworkTables.getValue('/SmartDashboard/BuildData/git-desc', 0));


	updateColors();

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
		console.log(v, $(v).text())
	});
}