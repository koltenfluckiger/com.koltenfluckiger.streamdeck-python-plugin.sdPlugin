let timeout = null;

function executeEvent(event, action, context, payload) {
  if (websocket) {
    const json = {
      "action": action,
      "event": event,
      "context": context,
      "payload": payload
    };
    websocket.send(JSON.stringify(json));
  }
}

function registerWebsocket(inRegisterEvent, uuid) {
  var json = {
    "event": inRegisterEvent,
    "uuid": uuid
  };
  websocket.send(JSON.stringify(json));
}

function logMessage(message) {
  var json = {
    "event": "logMessage",
    "payload": {
      "message": message
    }
  };
  websocket.send(JSON.stringify(json));
}

function setFilePath() {
  const filePath = document.getElementById('elgfilepicker');
  const decodedFilePath = decodeURIComponent(filePath.value.replace(/^C:\\fakepath\\/, ''));
  const realFilePath = decodedFilePath.replace(/(\/)/g, '\\');
  const fileInfo = document.getElementById('filelocation');
  fileInfo.value = realFilePath;
  fileInfo.textContent = realFilePath;
  updateSettings();
}

function saveSettings(context) {
  var payload = {};
  const nodes = document.querySelectorAll('.sdpi-item-value');
  for (const node of nodes) {
    if (node.id === "returnflag") {
      const value = node.checked;
      const id = node.id;
      payload[id] = value;
    } else {
      const value = ((node.value === undefined) ? "" : node.value);
      const id = node.id;
      payload[id] = value;
    }
  }
  if (websocket) {
    const json = {
      "event": "setSettings",
      "context": context,
      "payload": payload
    }
    console.log(json);
    websocket.send(JSON.stringify(json));
  }
}

function saveGlobalSettings(action, uuid, context) {
  var payload = {};
  const nodes = document.querySelectorAll('.sdpi-item-value');
  for (const node of nodes) {
    const value = node.value;
    const id = node.id;
    payload[id] = value;
  }
  cache[uuid] = {
    ...payload
  };
  if (websocket) {
    const json = {
      "action": action,
      "event": "setGlobalSettings",
      "context": uuid,
      "payload": payload
    }
    console.log(json);
    websocket.send(JSON.stringify(json));
  }
}

function requestGlobalSettings(context) {
  if (websocket) {
    var json = {
      'event': 'getGlobalSettings',
      'context': context
    };

    websocket.send(JSON.stringify(json));
  }
}

function requestSettings(context) {
  if (websocket) {
    var json = {
      'event': 'getSettings',
      'context': context
    };

    websocket.send(JSON.stringify(json));
  }
}


function onComplete(){
  clearTimeout(timeout);
  timeout = setTimeout(function () {
    updateSettings()
  }, 250);
}
