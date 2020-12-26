import Vue from "vue";
import VueSocketIO from "vue-socket.io";

Vue.use(
  new VueSocketIO({
    debug: true,
    connection: "/",
    options: { path: "/api/socket.io" },
  })
);
