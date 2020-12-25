<template>
  <div>
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
  </div>
</template>

<script>
export default {
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
    },
  },
};
</script>

<style lang="scss" scoped></style>
