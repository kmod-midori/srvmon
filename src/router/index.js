import Vue from "vue";
import VueRouter from "vue-router";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    name: "Home",
    component: () => import(/* webpackChunkName: "home" */ "../views/Home.vue"),
  },
  {
    path: "/login",
    name: "Login",
    meta: { unauth: true },
    component: () =>
      import(/* webpackChunkName: "login" */ "../views/Login.vue"),
  },
  {
    path: "/servers/add",
    name: "Add Server",
    component: () =>
      import(/* webpackChunkName: "add_server" */ "../views/AddServer.vue"),
  },
  {
    path: "/servers",
    name: "Servers",
    component: () =>
      import(/* webpackChunkName: "servers" */ "../views/Servers.vue"),
  },
  {
    path: "/contacts/add",
    name: "Add Contact",
    component: () =>
      import(/* webpackChunkName: "add_contact" */ "../views/AddContact.vue"),
  },
  {
    path: "/contacts",
    name: "Contacts",
    component: () =>
      import(/* webpackChunkName: "contacts" */ "../views/Contacts.vue"),
  },
  {
    path: "/settings",
    name: "Settings",
    component: () =>
      import(/* webpackChunkName: "settings" */ "../views/Settings.vue"),
  },
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes,
});

export default router;
