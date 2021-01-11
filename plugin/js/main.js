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

// Global cache
var cache = {};

// Global settings
var globalSettings = {};

// Setup the websocket and handle communication
function connectElgatoStreamDeckSocket(inPort, inPluginUUID, inRegisterEvent, inInfo) {
  var actions = {};
  websocket = new WebSocket('ws://127.0.0.1:' + inPort);
  websocket.onopen = function() {
    // WebSocket is connected, register the plugin
    var json = {
      "event": inRegisterEvent,
      "uuid": inPluginUUID
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

    if (event === 'didReceiveSettings') {
      var json = {
        "action": action,
        "event": "sendToPropertyInspector",
        "context": context,
        "payload": payload.settings
      };
      websocket.send(JSON.stringify(json));
    }
    else if (event === 'propertyInspectorDidAppear') {
      var settings = {
        'event': 'getSettings',
        'context': context
      };
      websocket.send(JSON.stringify(settings));
    }
  };
}
