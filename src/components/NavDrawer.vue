<template>
  <v-navigation-drawer :value="value" @change="emit('change', $event)" app>
    <v-list nav dense>
      <v-list-item v-for="item in items" :key="item.title" :to="item.to">
        <v-list-item-icon>
          <v-icon>{{ item.icon }}</v-icon>
        </v-list-item-icon>
        <v-list-item-title>{{ item.title }}</v-list-item-title>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>
</template>

<script>
export default {
  props: {
    value: {
      type: Boolean,
      default: false,
    },
  },
  data: () => ({
    items: [
      {
        icon: "mdi-server",
        title: "Servers",
        to: "/",
      },
      {
        icon: "mdi-contacts",
        title: "Contacts",
        to: "/contacts",
      },
      {
        icon: "mdi-cog",
        title: "Settings",
        to: "/settings",
      },
    ],
  }),
};
</script>
