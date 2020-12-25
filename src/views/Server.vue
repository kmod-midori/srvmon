<template>
  <div>
    <v-row>
      <v-col sm="12" md="6">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-server</v-icon>
            {{ server.label }}
          </v-card-title>
          <v-card-subtitle>
            Mode: {{ modes[server.mode] }}<br />
            <template v-if="server.mode === 'active-http'">
              Test URL: <a :href="server.config.url">{{ server.config.url }}</a>
              <br />
              Valid status codes: {{ server.config.validStatus.join(", ") }}
            </template>
          </v-card-subtitle>
          <v-card-actions>
            <v-btn icon :to="`/servers/${id}/edit`">
              <v-icon>mdi-cog</v-icon>
            </v-btn>
            <v-spacer />
            <v-chip
              :color="server.enabled ? 'success' : 'grey'"
              @click="toggleEnabled"
            >
              <v-progress-circular
                v-if="enabledToggling"
                indeterminate
                size="16"
                class="mr-2"
              ></v-progress-circular>
              {{ server.enabled ? "Enabled" : "Disabled" }}
            </v-chip>
          </v-card-actions>
        </v-card>
      </v-col>

      <v-col sm="12" md="6">
        <v-card class="mt-1">
          <v-card-title>
            <v-icon left>mdi-speedometer</v-icon>
            Status
          </v-card-title>
        </v-card>
      </v-col>
    </v-row>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: parseInt(this.$route.params.id, 10),
      server: {},
      enabled: false,
      enabledToggling: false,
      modes: {
        "passive-http": "Passive HTTP",
        "active-http": "Active HTTP",
        "active-tcp": "Active TCP",
      },
    };
  },
  mounted() {
    this.loadServer();
  },
  methods: {
    loadServer() {
      this.$http.get(`/servers/${this.id}`).then((resp) => {
        this.setServer(resp.data.payload);
      });
    },
    toggleEnabled() {
      this.enabledToggling = true;
      this.$http
        .post(`/servers/${this.id}`, { enabled: !this.server.enabled })
        .then((resp) => {
          this.setServer(resp.data.payload);
        })
        .finally(() => {
          this.enabledToggling = false;
        });
    },
    setServer(server) {
      this.server = server;
      this.enabled = this.server.enabled;
    },
  },
};
</script>
