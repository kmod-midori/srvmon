import Vue from "vue";
import axios from "axios";

const instance = axios.create({ baseUrl: "/api" });

Vue.prototype.$http = instance;
