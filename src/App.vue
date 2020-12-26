<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>
        Server Monitor <span v-if="$route.name"> - {{ $route.name }}</span>
      </v-toolbar-title>

      <v-spacer></v-spacer>
      <UserControl />
    </v-app-bar>

    <NavDrawer v-model="drawer" />

    <v-main>
      <v-container fluid><router-view /></v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavDrawer from "@/components/NavDrawer";
import UserControl from "@/components/UserControl";

export default {
  name: "App",

  components: {
    NavDrawer,
    UserControl,
  },

  data: () => ({
    drawer: false,
  }),
};
</script>
