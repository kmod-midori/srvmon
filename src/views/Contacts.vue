<template>
  <div>
    <v-card v-for="item in contacts" :key="item.id" class="mb-2">
      <v-card-title>
        <v-icon left>{{ types[item.type].icon }}</v-icon>
        {{ types[item.type].name }}
      </v-card-title>

      <template v-if="item.type === 'email'">
        <v-list-item>
          <v-list-item-title>Address</v-list-item-title>
          <v-list-item-subtitle>
            <a :href="'mailto:' + item.config.address">
              {{ item.config.address }}
            </a>
          </v-list-item-subtitle>
        </v-list-item>
      </template>

      <template v-else-if="item.type === 'webhook'">
        <v-list-item>
          <v-list-item-title>URL</v-list-item-title>
          <v-list-item-subtitle>
            <a :href="item.config.url">{{ item.config.url }}</a>
          </v-list-item-subtitle>
        </v-list-item>
        <v-list-item>
          <v-list-item-title>Mode</v-list-item-title>
          <v-list-item-subtitle>
            {{ webhookServices[item.config.service] }}
          </v-list-item-subtitle>
        </v-list-item>
      </template>

      <v-card-actions>
        <v-spacer></v-spacer>
        <v-btn
          v-if="item.enabled"
          icon
          color="success"
          @click="setEnabled(item.id, false)"
        >
          <v-icon>mdi-bell</v-icon>
        </v-btn>
        <v-btn v-else icon @click="setEnabled(item.id, true)">
          <v-icon>mdi-bell-off</v-icon>
        </v-btn>
        <v-btn icon color="error" @click="deleteItem(item.id)">
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
      contacts: [],
      types: {
        email: {
          name: "Email",
          icon: "mdi-email",
        },
        webhook: {
          name: "Webhook",
          icon: "mdi-webhook",
        },
      },
      webhookServices: {
        ding: "DingTalk",
        discord: "Discord",
      },
    };
  },
  mounted() {
    this.load();
  },
  methods: {
    async load() {
      const resp = await this.$http.get("/contacts");
      this.contacts = resp.data.payload.contacts;
    },
    async setEnabled(id, enabled) {
      const resp = await this.$http.post(`/contacts/${id}`, {
        enabled: enabled,
      });
      await this.load();
    },
    async deleteItem(id) {
      const resp = await this.$http.delete(`/contacts/${id}`);
      await this.load();
    },
  },
};
</script>
