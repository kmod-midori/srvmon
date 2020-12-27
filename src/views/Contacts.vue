<template>
  <div>
    <v-card v-for="item in contacts" :key="item.id" class="mb-2">
      <v-card-title>
        <v-icon left>mdi-{{ item.type }}</v-icon>
        {{ item.type }}
      </v-card-title>
      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn v-if="item.enabled" icon color="success">
          <v-icon>mdi-bell</v-icon>
        </v-btn>
        <v-btn v-else icon>
          <v-icon>mdi-bell-off</v-icon>
        </v-btn>
        <v-btn icon color="error">
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </v-card-actions>
    </v-card>

    <v-fab-transition>
      <v-btn fab fixed bottom right dark to="/contacts/add">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
  </div>
</template>

<script>
export default {
  data() {
    return {
      contacts: [
        {
          id: 1,
          type: "webhook",
          enabled: true,
        },
        {
          id: 2,
          type: "email",
          enabled: false,
        },
      ],
    };
  },
};
</script>

