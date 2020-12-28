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

          <template v-else-if="server.mode === 'active-tcp'">
            <v-list-item>
              <v-list-item-title>Test Address</v-list-item-title>
              <v-list-item-subtitle>
                {{ server.config.address }}:{{ server.config.port }}
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
            <v-chip v-if="server.watching" color="success" @click="unwatch">
              <v-avatar left><v-icon>mdi-bell</v-icon></v-avatar>
              Watching
            </v-chip>
            <v-chip v-else color="grey" @click="watch">
              <v-avatar left><v-icon>mdi-bell-off</v-icon></v-avatar>
              Not Watching
            </v-chip>
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
            <StatusIndicator class="ml-2" :online="online" />
          </v-card-title>

          <v-list-item v-if="lastChecked">
            <v-list-item-title>Last Checked</v-list-item-title>
            <v-list-item-subtitle>{{
              lastChecked | luxon("yyyy-MM-dd HH:mm:ss")
            }}</v-list-item-subtitle>
          </v-list-item>
        </v-card>
      </v-col>
    </v-row>

    <v-card>
      <v-card-title>
        <v-icon left>mdi-clock</v-icon>
        History
      </v-card-title>
      <v-data-table :headers="recordHeaders" :items="records">
        <template v-slot:item.time="{ item }">
          {{ item.time | luxon("yyyy-MM-dd HH:mm:ss") }}
        </template>
        <template v-slot:item.online="{ item }">
          <StatusIndicator :online="item.online" />
          <span v-if="item.message" class="ml-1">{{ item.message }}</span>
        </template>
      </v-data-table>
    </v-card>
  </div>
</template>

<script>
import StatusIndicator from "@/components/StatusIndicator";
export default {
  components: { StatusIndicator },
  data() {
    return {
      id: parseInt(this.$route.params.id, 10),
      server: { config: {} },
      enabledToggling: false,
      modes: {
        "passive-http": "Passive HTTP",
        "active-http": "Active HTTP",
        "active-tcp": "Active TCP",
      },
      records: [],
      recordHeaders: [
        {
          text: "Time",
          value: "time",
        },
        {
          text: "Status",
          value: "online",
        },
        {
          text: "Latency (ms)",
          value: "latency",
        },
      ],
    };
  },
  sockets: {
    connect() {
      this.startMon();
    },
    new_record(record) {
      if (record.server_id !== this.id) return;
      for (const rec of this.records) {
        if (rec.id === record.id) {
          return;
        }
      }
      this.records.unshift(record);
      if (this.records.length > 50) {
        // Truncate to 50
        this.records = this.records.slice(0, 50);
      }
    },
  },
  mounted() {
    this.loadServer();
    this.loadRecords();
    this.startMon();
  },
  destroyed() {
    this.$socket.emit("stop_mon", { id: this.id });
  },
  methods: {
    startMon() {
      this.$socket.emit("start_mon", { id: this.id });
    },
    async loadServer() {
      const resp = await this.$http.get(`/servers/${this.id}`);
      this.server = resp.data.payload;
    },
    async loadRecords() {
      const resp = await this.$http.get(
        `/servers/${this.id}/records?itemsPerPage=10`
      );
      this.records = resp.data.payload.items;
    },
    async toggleEnabled() {
      this.enabledToggling = true;
      try {
        await this.$http.post(`/servers/${this.id}`, {
          enabled: !this.server.enabled,
        });
        this.loadServer();
      } finally {
        this.enabledToggling = false;
      }
    },
    async watch() {
      await this.$http.put(`/servers/${this.id}/watch`);
      this.loadServer();
    },
    async unwatch() {
      await this.$http.delete(`/servers/${this.id}/watch`);
      this.loadServer();
    },
  },
  computed: {
    online() {
      if (this.records.length === 0) return null;
      return this.records[0].online;
    },
    lastChecked() {
      if (this.records.length === 0) return 0;
      return this.records[0].time;
    },
  },
};
</script>
