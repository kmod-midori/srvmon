<template>
  <span>
    <v-chip v-if="online" color="success">
      <v-avatar left>
        <v-icon small>mdi-server</v-icon>
      </v-avatar>
      Online
    </v-chip>
    <v-chip v-else-if="online === null" color="grey">
      <v-avatar left>
        <v-icon small>mdi-server-remove</v-icon>
      </v-avatar>
      Unknown
    </v-chip>
    <v-chip v-else color="error">
      <v-avatar left>
        <v-icon small>mdi-server-remove</v-icon>
      </v-avatar>
      Offline
    </v-chip>
  </span>
</template>

<script>
export default {
  props: ["online"],
};
</script>

<style lang="scss" scoped></style>
