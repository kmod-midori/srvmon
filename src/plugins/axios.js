import Vue from "vue";
import axios from "axios";
import router from "../router";
import toast from "./notification";

const instance = axios.create({ baseURL: "/api", maxRedirects: 0 });

instance.interceptors.response.use(
  function (resp) {
    console.log(resp);
    return resp;
  },
  function (err) {
    if (err.response.status === 401) {
      const matched = router.currentRoute.matched[0] || {};
      const meta = matched.meta || {};

      if (!meta.unauth) {
        router.replace("/login");
        return;
      }
    }
    let payload = err.response.data.payload;
    if (payload && payload.error) {
      toast("error", payload.error);
    } else {
      toast("error", err.toString());
    }
    return Promise.reject(err);
  }
);

Vue.prototype.$http = instance;

export default instance;
