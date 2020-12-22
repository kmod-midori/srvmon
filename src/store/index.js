import Vue from "vue";
import Vuex from "vuex";
import axios from "../plugins/axios";

Vue.use(Vuex);

const user = {
  state: () => ({
    user: null,
  }),
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
  },
  actions: {
    async init({ commit }) {
      try {
        const res = await axios.get("accounts/current");
        commit("setUser", res.data.payload);
      } catch (err) {
        console.info("Not logged in");
      }
    },
    async login({ dispatch }, req) {
      await axios.post("accounts/login", req);
      await dispatch("init");
    },
  },
  getters: {
    loggedIn: (state) => state.user !== null,
  },
  namespaced: true,
};

export default new Vuex.Store({
  state: {},
  mutations: {},
  actions: {},
  modules: { user },
});
