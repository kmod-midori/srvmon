import Vue from "vue";
import VueSocketIO from "vue-socket.io";

const socket = new VueSocketIO({
  debug: true,
  connection: "/",
  options: { path: "/api/socket.io" },
});

Vue.use(socket);

export default socket;
