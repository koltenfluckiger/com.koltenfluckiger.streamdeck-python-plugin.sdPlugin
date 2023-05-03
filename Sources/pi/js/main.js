//==============================================================================
/**
@file       main.js
@brief      Kolten Fluckiger
**/
//==============================================================================

var websocket = null;
var UUID = null;
var context = null;
var cache = {};

function connectElgatoStreamDeckSocket(port, pluginUUID, registerEvent, inInfo, inActionInfo) {

  var actionInfo = JSON.parse(inActionInfo);
  var info = JSON.parse(inInfo);
  var action = actionInfo['action']

  UUID = pluginUUID;

  websocket = new WebSocket('ws://127.0.0.1:' + port);
  websocket.onopen = function() {
    registerWebsocket(registerEvent, UUID);
    requestSettings(UUID)
  };

  websocket.onmessage = function(evt) {

    const obj = JSON.parse(evt.data);
    const event = obj['event'];
    const payload = obj['payload'];

    if (event === 'didReceiveSettings') {
      try {
        const settings = payload.settings;

        const filelocation = document.getElementById('filelocation');
        const arguments = document.getElementById('arguments');
        const returnflag = document.getElementById('returnflag');

        filelocation.value = settings.filelocation;
        filelocation.textContent = settings.filelocation;
        arguments.value = settings.arguments ? settings.arguments : "";
        returnflag.checked = settings.returnflag;

      } catch (err) {
        console.log(err)
      }
    }
  };

  this.updateSettings = function() {
    saveSettings(UUID);
  }
}
