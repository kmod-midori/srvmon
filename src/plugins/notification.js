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

export default toast;
