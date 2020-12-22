<template>
  <v-app>
    <v-app-bar app color="primary" dark collapse-on-scroll>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>
        Server Monitor <span v-if="$route.name"> - {{ $route.name }}</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <v-menu v-if="user" open-on-hover offset-y>
        <template v-slot:activator="{ on, attrs }">
          <v-btn dark v-bind="attrs" v-on="on" text>
            {{ user.email }}
          </v-btn>
        </template>
        <v-list>
          <v-list-item link @click="logout">
            <v-list-item-title>Logout</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
    </v-app-bar>

    <NavDrawer v-model="drawer" />

    <v-main>
      <v-container fluid><router-view /></v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavDrawer from "@/components/NavDrawer";

export default {
  name: "App",

  components: {
    NavDrawer,
  },

  data: () => ({
    drawer: false,
  }),

  mounted() {
    this.$store.dispatch("user/init");
  },
  computed: {
    user() {
      return this.$store.state.user.user || {};
    },
  },
  methods: {
    async logout() {
      await this.$http.post("/accounts/logout");
      this.$router.go("/login");
    }
  }
};
</script>
