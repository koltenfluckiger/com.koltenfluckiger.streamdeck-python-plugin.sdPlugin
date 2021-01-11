//==============================================================================
/**
@file       main.js
@brief      Philips Hue Plugin
@copyright  (c) 2019, Corsair Memory, Inc.
            This source code is licensed under the MIT-style license found in the LICENSE file.
**/
//==============================================================================

// Global web socket
var websocket = null;
var inPropertyInspectorUUID = null;
var inRegisterEvent = null;
var inInfo = null;
var inActionInfo = null;
var cache = {};
var globalSettings = {};
var settings = {};

// Setup the websocket and handle communication
function connectElgatoStreamDeckSocket(inPort, inPropertyInspectorUUID, inRegisterEvent, inInfo, inActionInfo) {

  var actions = {};
  var actionInfo = JSON.parse(inActionInfo);
  var info = JSON.parse(inInfo);

  inPropertyInspectorUUID = inPropertyInspectorUUID;
  inRegisterEvent = inRegisterEvent;
  inInfo = inInfo;

  settings = actionInfo['payload']['settings'];

  websocket = new WebSocket('ws://127.0.0.1:' + inPort);
  websocket.onopen = function() {
    // WebSocket is connected, register the plugin
    var json = {
      "event": inRegisterEvent,
      "uuid": inPropertyInspectorUUID
    };

    websocket.send(JSON.stringify(json));
  };

  // Web socked received a message
  websocket.onmessage = function(evt) {

    const obj = JSON.parse(evt.data);
    const event = obj['event'];
    const action = obj['action'];
    const context = obj['context'];
    const payload = obj['payload'];


    if(event === 'sendToPropertyInspector'){
      const fileLocation = document.getElementById('file_location');
      const arguments = document.getElementById('arguments');
      fileLocation.value = payload.fileLocation;
      arguments.value = payload.arguments;
    }
  };

  this.updateSettings = function() {
    const fileLocation = document.getElementById('dummy_file_location').value;
    const arguments = document.getElementById('arguments').value;
    console.log(fileLocation);
    const json = {
      "action": inActionInfo['action'],
      "event": "setSettings",
      "context": inPropertyInspectorUUID,
      "payload": {
        "fileLocation": fileLocation,
        "arguments": arguments
      }
    }
    websocket.send(JSON.stringify(json));
  }
}
