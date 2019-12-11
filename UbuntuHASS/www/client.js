#!/usr/bin/env node
const WebSocket = require('ws');
var ws = new WebSocket("ws://192.168.53.2:7688", "socketServerWEBS");
var msg = process.argv[2];

ws.onopen = function(evt) {
  console.log("Connection open ...");
  ws.send(msg);
  console.log("send: " + msg)
  ws.terminate();
  //ws.close();
};

ws.onmessage = function(evt) {
  console.log("Received Message: " + evt.data);
}

ws.onclose = function(evt) {
  console.log("Connection closed ...");
}

