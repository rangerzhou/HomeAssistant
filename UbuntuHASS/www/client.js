#!/usr/bin/env node
const WebSocket = require('ws');
var ws = new WebSocket("ws://localhost:7999", "socketServerWEBS");
var msg = process.argv[2];

ws.onopen = function(evt) { 
  console.log("Connection open ..."); 
  //ws.send("AAPH,80020001,1234,HelloWorld");
  ws.send(msg);
  console.log("send: " + msg); 
  //ws.close();
  ws.terminate();
};

ws.onmessage = function(evt) {
  console.log( "Received Message: " + evt.data);
  //ws.close();
};

ws.onclose = function(evt) {
  console.log("Connection closed.");
};

