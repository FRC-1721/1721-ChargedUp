// Require all
let url135 = require("url:./assets/sounds/135.wav");
let url100 = require("url:./assets/sounds/100.wav");
let url70 = require("url:./assets/sounds/70.wav");
let url50 = require("url:./assets/sounds/50.wav");
let url30 = require("url:./assets/sounds/30.wav");
let url20 = require("url:./assets/sounds/20.wav");
let url10 = require("url:./assets/sounds/10.wav");
let url9 = require("url:./assets/sounds/9.wav");
let url8 = require("url:./assets/sounds/8.wav");
let url7 = require("url:./assets/sounds/7.wav");
let url6 = require("url:./assets/sounds/6.wav");
let url5 = require("url:./assets/sounds/5.wav");
let url4 = require("url:./assets/sounds/4.wav");
let url3 = require("url:./assets/sounds/3.wav");
let url2 = require("url:./assets/sounds/2.wav");
let url1 = require("url:./assets/sounds/1.wav");



export function countDownAlerts(key, value) {
    /* Updates on every match time update */
    let keys = [[135, url135], [100, url100], [70, url70], [50, url50], [30, url30], [20, url20],
    [10, url10],
    [9, url9],
    [8, url8],
    [7, url7],
    [6, url6],
    [5, url5],
    [4, url4],
    [3, url3],
    [2, url2],
    [1, url1],];

    for (var i = 0; i < keys.length; i++) {
        if (keys[i][0] == value) {
            let audio = new Audio(keys[i][1]);
            audio.play();
        }
    }
}
