<template>
  <div>
    <v-data-table
      :headers="headers"
      :items="servers"
      :loading="loading"
      :options.sync="options"
      :server-items-length="totalServers"
      class="elevation-1"
    >
      <template v-slot:item.label="{ item }">
        <router-link :to="`/servers/${item.id}`">
          {{ item.label }}
        </router-link>
      </template>
      <template v-slot:item.enabled="{ item }">
        <v-chip :color="item.enabled ? 'success' : 'grey'" dark>
          {{ item.enabled ? "Yes" : "No" }}
        </v-chip>
      </template>
      <template v-slot:item.lastRecord="{ item }">
        <template v-if="item.lastRecord">
          <StatusIndicator :online="item.lastRecord.online" />
          {{ item.lastRecord.time | luxon }}
        </template>
        <template v-else>
          <StatusIndicator :online="null" />
        </template>
      </template>
    </v-data-table>

    <v-fab-transition>
      <v-btn fab fixed bottom right dark to="/servers/add">
        <v-icon>mdi-plus</v-icon>
      </v-btn>
    </v-fab-transition>
  </div>
</template>

<script>
import StatusIndicator from "@/components/StatusIndicator";
export default {
  components: { StatusIndicator },
  data() {
    return {
      headers: [
        {
          text: "Server",
          value: "label",
        },
        {
          text: "Enabled",
          value: "enabled",
        },
        {
          text: "Last Checked",
          sortable: false,
          value: "lastRecord",
        },
      ],

      servers: [],
      loading: false,
      totalServers: 0,
      options: {
        page: 1,
        itemsPerPage: 10,
      },
    };
  },
  mounted() {
    this.loadServers();
  },
  methods: {
    async loadServers() {
      this.loading = true;
      this.$http
        .get("/servers", {
          params: {
            with_status: true,
            ...this.options,
          },
        })
        .then((resp) => {
          const payload = resp.data.payload;
          this.servers = payload.items;
          this.totalServers = payload.total;
        })
        .finally(() => {
          this.loading = false;
        });
    },
  },
  watch: {
    options: {
      handler() {
        this.loadServers();
      },
      deep: true,
    },
  },
};
</script>

<style lang="scss" scoped></style>
