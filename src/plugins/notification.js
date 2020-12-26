import Vue from "vue";
import Noty from "noty"; // https://github.com/needim/noty
import "noty/lib/noty.css";
import "noty/lib/themes/mint.css";

function toast(type, message, timeout = 3000) {
  if (type === "warn") type = "warning";
  return new Noty({
    text: message,
    type,
    timeout,
  }).show();
}

Vue.prototype.$notify = toast;

async function requestNativePermission() {
  if (!("Notification" in window) || Notification.permission === "denied") {
    return false;
  }

  if (Notification.permission !== "granted") {
    await Notification.requestPermission();
  }

  return Notification.permission === "granted";
}

Vue.prototype.$notifyNative = async function (title) {
  if (await requestNativePermission()) {
    new Notification("Server Monitor", {
      body: title,
    });
  }
};

document.addEventListener("load", function () {
  if (requestNativePermission()) {
    console.info("Notification permission granted.");
  }
});

export default toast;
