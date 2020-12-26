<template>
  <div>
    <v-row>
      <v-col cols="12" lg="6">
        <v-card>
          <v-card-title>
            <v-icon left>mdi-server</v-icon>
            {{ server.label }}
          </v-card-title>
          <v-list-item>
            <v-list-item-title>Mode</v-list-item-title>
            <v-list-item-subtitle>
              {{ modes[server.mode] }}
            </v-list-item-subtitle>
          </v-list-item>

          <template v-if="server.mode === 'active-http'">
            <v-list-item>
              <v-list-item-title>Test URL</v-list-item-title>
              <v-list-item-subtitle>
                <a :href="server.config.url">{{ server.config.url }}</a>
              </v-list-item-subtitle>
            </v-list-item>
            <v-list-item>
              <v-list-item-title>Valid Status Codes</v-list-item-title>
              <v-list-item-subtitle>
                {{ server.config.validStatus.join(", ") }}
              </v-list-item-subtitle>
            </v-list-item>
          </template>

          <v-list-item>
            <v-list-item-title>Interval</v-list-item-title>
            <v-list-item-subtitle>
              {{ server.config.interval }} seconds
            </v-list-item-subtitle>
          </v-list-item>

          <v-list-item v-if="server.mode !== 'passive-http'">
            <v-list-item-title>Timeout</v-list-item-title>
            <v-list-item-subtitle>
              {{ server.config.timeout }} ms
            </v-list-item-subtitle>
          </v-list-item>

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

      <v-col cols="12" lg="6">
        <v-card class="mt-1">
          <v-card-title>
            <v-icon left>mdi-speedometer</v-icon>
            Status
            <v-chip v-if="online" class="ml-2" color="success">
              <v-avatar left>
                <v-icon small>mdi-server</v-icon>
              </v-avatar>
              Online
            </v-chip>
            <v-chip v-else class="ml-2" color="error">
              <v-avatar left>
                <v-icon small>mdi-server-remove</v-icon>
              </v-avatar>
              Offline
            </v-chip>
          </v-card-title>

          <v-list-item>
            <v-list-item-title>Last Checked</v-list-item-title>
            <v-list-item-subtitle> 5 minutes ago </v-list-item-subtitle>
          </v-list-item>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn
              v-if="server.mode !== 'passive-http'"
              icon
              @click="scheduleCheck"
            >
              <v-icon>mdi-refresh</v-icon>
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
    <v-card>
      <v-card-title>
        <v-icon left>mdi-clock</v-icon>
        History
      </v-card-title>
    </v-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      id: parseInt(this.$route.params.id, 10),
      server: { config: {} },
      enabled: false,
      enabledToggling: false,
      modes: {
        "passive-http": "Passive HTTP",
        "active-http": "Active HTTP",
        "active-tcp": "Active TCP",
      },
      online: false,
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
    scheduleCheck() {
      this.$notify("success", "Check scheduled");
    },
  },
};
</script>
