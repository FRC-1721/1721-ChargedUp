"use strict";

import { countDownAlerts } from "./audioAlerts";

let epilepsy = false;
let epilepsyAmount = 0;

$(function () {
    // sets a function that will be called when the websocket connects/disconnects
    NetworkTables.addWsConnectionListener(onNetworkTablesConnection, true);

    // sets a function that will be called when the robot connects/disconnects
    NetworkTables.addRobotConnectionListener(onRobotConnection, true);

    // sets a function that will be called when any NetworkTables key/value changes
    NetworkTables.addGlobalListener(onValueChanged, true);

    loadCameraOnConnect({
        container: "#cam1", // id of camera div
        proto: null, // url scheme
        host: "10.17.21.11", // ip
        port: 5800,
        image_url: "/",
        data_url: "/",
        wait_img: require("./assets/no_signal.png"),
        error_img: require("./assets/error.png"),
        attrs: {
            width: 320,
            height: 240,
        },
    });

    loadCameraOnConnect({
        container: "#cam2",
        proto: null,
        host: "10.17.21.13",
        port: 5800,
        image_url: "/",
        data_url: "/",
        wait_img: require("./assets/no_signal.png"),
        error_img: require("./assets/error.png"),
        attrs: {
            width: 320,
            height: 240,
        },
    });
});

$(document).on("input", ".dub-slider", function () {
    NetworkTables.putValue($(this).data("key"), parseFloat($(this).val()));
});

$(document).on("click", "#aut-sel > button", function () {
    // YOU NEED to put the value in Autonomous/selected NOT Autonomous/active or it won't stay
    NetworkTables.putValue(
        "/SmartDashboard/Autonomous/selected",
        $(this).html()
    );
});

$("#p-sw").change(function () {
    if (this.checked) {
        $("*").addClass("pink");
        $("#p-sw-l").removeClass("pink");
        $("#p-sw-s").removeClass("pink");
        $("#p-sw-l").css("background", "#c3768b");
        $("#p-sw-s").css("background", "#b3667b");
    } else {
        $("*").removeClass("pink");
        $("#p-sw-l").css("background", "");
        $("#p-sw-s").css("background", "");
    }
});

function onRobotConnection(connected) {
    $("#robotstate").text(connected ? "Connected" : "Disconnected");
    $("#robotAddress").text(
        connected ? NetworkTables.getRobotAddress() : "Disconnected"
    );

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
        var tr = $('<div class="table-info"></div>').appendTo(
            $("#nt > .table")
        );
        $('<div class="table-label"></div>').text(key).appendTo(tr);
        $('<div class="table-area"></div>')
            .attr("id", NetworkTables.keyToId(key))
            .text(value)
            .appendTo(tr);
    } else {
        // similarly, use keySelector to convert the key to a valid jQuery
        // selector. This should work for class names also, not just for ids
        $("#" + NetworkTables.keySelector(key)).text(value);
    }

    updateColors();

    $(".dub-slider").each(function () {
        $(this).val(NetworkTables.getValue($(this).data("key")));
    });

    $(".dub-text").each(function () {
        $(this).text(NetworkTables.getValue($(this).data("key")));
    });

    if (key.includes("/SmartDashboard/Audio")) {
        countDownAlerts(key, value);
    }

    if (key === "/SmartDashboard/Autonomous/options") {
        var options = NetworkTables.getValue(
            "/SmartDashboard/Autonomous/options"
        );
        $("#aut-sel").empty();
        options.forEach((v, i) => {
            $("<button></button>")
                .attr("id", "opt" + i)
                .html(v)
                .appendTo($("#aut-sel"));
        });
    }

    $("#aut-sel > button").each(function () {
        if (
            $(this).html() ==
            NetworkTables.getValue("/SmartDashboard/Autonomous/active")
        ) {
            $(this).css("background", "#802");
        } else {
            $(this).css("background", "#3c3836");
        }
    });

    if (key.includes("/SmartDashboard/Pose/Pose")) {
        updateRobotPos(NetworkTables.getValue(key), key.substr(key.length - 1));
    }
}

function highlightColor(id, hex, norm = "#504945") {
    if (hex === norm) {
        $(id).css("background", "norm");
    } else {
        $(id).css(
            "background",
            "linear-gradient(to right, " + norm + ", " + hex + ")"
        );
    }
}

function checkSenTableVal(patt, id, hex, overwrite = true, norm = "#504945") {
    if (patt.test($(id).text())) {
        highlightColor(id, hex);
    } else if (overwrite) {
        highlightColor(id, norm);
    }
}

function updateColors() {
    const ids = ["#connectstate", "#robotstate", "#robotAddress"];
    ids.forEach((v, _) => {
        if ($(v).text() == "Unknown") {
            highlightColor(v, "#cc241d");
        } else if ($(v).text() == "Disconnected") {
            highlightColor(v, "#cc241d");
        } else {
            highlightColor(v, "#689d6a");
        }
    });

    // Custom formatting
    checkSenTableVal(/-dirty$/, "#git-hash-area", "#cc241d");

    // Programmers
    checkSenTableVal(/SimUser$/, "#builder-area", "#d3869b"); // First one is fine to overwrite.
    checkSenTableVal(/joe/, "#builder-area", "#831598", false);
    checkSenTableVal(/dylan/, "#builder-area", "#fe8019", false);
    checkSenTableVal(/kredcool/, "#builder-area", "#67ab24", false);

    // Branches
    checkSenTableVal(
        /event/,
        "#git-branch-area",
        "linear-gradient(to right, #504945, #689d6a)"
    );
    checkSenTableVal(
        /sim/,
        "#git-branch-area",
        "linear-gradient(to right, #504945, #cc241d)",
        false
    );

    // Checks if DashHash™ is the same as the Robot's git hash
    if (
        $("#git-hash-area").text().slice(0, $("#dash-hash").text().length) ===
        $("#dash-hash").text()
    ) {
        highlightColor("#dash-hash", "#504945");
    } else {
        highlightColor("#dash-hash", "#fabd2f");
    }

	
	// Custom formatting
	highlightColor(/-dirty$/, "#git-hash-area", 'linear-gradient(to right, #504945, #cc241d)');

	// Programmers
	highlightColor(/SimUser$/, "#builder-area", 'linear-gradient(to right, #504945, #d3869b)'); // First one is fine to overwrite.
	highlightColor(/joe/, "#builder-area", 'linear-gradient(to right, #504945, #831598)', false);
	highlightColor(/dylan/, "#builder-area", 'linear-gradient(to right, #504945, #fe8019)', false);


	// Branches
	highlightColor(/event/, "#git-branch-area", 'linear-gradient(to right, #504945, #689d6a)');
	highlightColor(/sim/, "#git-branch-area", 'linear-gradient(to right, #504945, #cc241d)', false);

}

// p5.js canvas

function getRandomInt(min, max) {
    return Math.floor(Math.random() * (max - min + 1)) + min;
}

// img -> background image
// joe, dvd -> floating distraction images
let img, joe, dvd;
let posX, posY, posT;

// floating distraction images position data
//               moving right (bool), moving down (bool) , posX                , posY
let bounceJoe = [
    Math.random() < 0.5,
    Math.random() < 0.5,
    getRandomInt(0, 753),
    getRandomInt(0, 341),
];
let bounceDvd = [
    Math.random() < 0.5,
    Math.random() < 0.5,
    getRandomInt(0, 681),
    getRandomInt(0, 328),
];

let running = true;

function preload() {
    // Images
    img = loadImage(require("./assets/field.png"));
    joe = loadImage(require("./assets/joe.png"));
    dvd = loadImage(require("./assets/dvd.png"));
}

function setup() {
    let canvas = createCanvas(777, 377);
    canvas.parent("field-canvas");
    frameRate(15);
}

function draw() {
    background(220);
    image(img, 0, 0);

    posX = NetworkTables.getValue("/SmartDashboard/Pose/Pose x");
    posY = NetworkTables.getValue("/SmartDashboard/Pose/Pose y");
    posT = NetworkTables.getValue("/SmartDashboard/Pose/Pose t");

    rectMode(CENTER);
    push();
    translate(posX * 0.46977025392987, 377 - posY * 0.46977025392987);
    translate(posX * 98.046638401, -posY * 98.046638401);
    rotate(radians(180 + posT));
    rotate(-posT);
    rect(0, 0, 24, 34);
    fill(color("#504945"));
    rect(0, 0, 34, 24);
    fill(color("#802"));
    rect(17, 0, 17, 24);
    pop();
    rectMode(CORNER);

    if ($("#p-sw").is(":checked")) {
        image(dvd, bounceDvd[2], bounceDvd[3]);
        image(joe, bounceJoe[2], bounceJoe[3]);
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
            96;
            bounceDvd[0] = !bounceDvd[0];
        }
        if (bounceDvd[3] < 0 || bounceDvd[3] > 328) {
            49;
            bounceDvd[1] = !bounceDvd[1];
        }
    }

    // Epilepsy
    if (epilepsy) {
        epilepsyAmount += 10;
        epilepsyAmount = epilepsyAmount > 360 ? 0 : epilepsyAmount;
        $(".epilepsy").css("filter", "hue-rotate(" + epilepsyAmount + "deg)");
    } else {
        epilepsyAmount = 0;
    }
}

function updateRobotPos(v, i) {
    window["pos" + i.toUpperCase()] = v;
}

window.preload = preload;
window.setup = setup;
window.draw = draw;
//window.mousePressed = mousePressed;
