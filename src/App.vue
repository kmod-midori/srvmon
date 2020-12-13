<template>
  <v-app>
    <v-app-bar app color="primary" dark collapse-on-scroll>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Server Monitor</v-toolbar-title>

      <v-spacer></v-spacer>
    </v-app-bar>

    <NavDrawer v-model="drawer" />

    <v-main>
      <v-container><router-view /></v-container>
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
};
</script>
