// Require all
let wavGlob = require("url:./assets/sounds/*.wav");

export function countDownAlerts(key, value) {
    /* Updates on every match time update */

    if (key.includes("MatchTime")) {
        if (wavGlob[value] != undefined) { // If one of the globbed files matches
            let audio = new Audio(wavGlob[value]); // Create the audio object

            // Play it!
            audio.play().catch(function (DOMException) { });
        }
    }
}
