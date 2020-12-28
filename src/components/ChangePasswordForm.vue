<template>
  <div>
    <v-form @submit.prevent="submit">
      <v-text-field
        v-model="password"
        label="Current Password"
        required
        :error-messages="passwordErrors"
        @input="$v.password.$touch()"
        @blur="$v.password.$touch()"
        type="password"
      ></v-text-field>
      <v-text-field
        v-model="newPassword"
        label="New Password"
        required
        :error-messages="newPasswordErrors"
        @input="$v.newPassword.$touch()"
        @blur="$v.newPassword.$touch()"
        type="password"
      ></v-text-field>
      <v-text-field
        v-model="retypePassword"
        label="Repear Password"
        required
        :error-messages="retypePasswordErrors"
        @input="$v.retypePassword.$touch()"
        @blur="$v.retypePassword.$touch()"
        type="password"
      ></v-text-field>
      <v-btn color="primary" :disabled="$v.$invalid" @click="submit">
        Submit
      </v-btn>
    </v-form>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, sameAs, minLength } from "vuelidate/lib/validators";

export default {
  mixins: [validationMixin],
  validations: {
    password: {
      required,
    },
    newPassword: {
      required,
      minLength: minLength(8),
    },
    retypePassword: {
      sameAs: sameAs("newPassword"),
    },
  },
  data() {
    return {
      password: "",
      newPassword: "",
      retypePassword: "",
    };
  },
  computed: {
    passwordErrors() {
      const errors = [];
      if (!this.$v.password.$dirty) return errors;
      !this.$v.password.required && errors.push("Password is required");
      return errors;
    },
    newPasswordErrors() {
      const errors = [];
      if (!this.$v.newPassword.$dirty) return errors;
      !this.$v.newPassword.required && errors.push("New password is required");
      !this.$v.newPassword.minLength &&
        errors.push("New password must be at least 8 characters");
      return errors;
    },
    retypePasswordErrors() {
      const errors = [];
      if (!this.$v.retypePassword.$dirty) return errors;
      !this.$v.retypePassword.sameAs && errors.push("Password does not match");
      return errors;
    },
  },
  methods: {
    async submit() {
      if (this.$v.$invalid) return;
      const form = {
        password: this.password,
        new_password: this.newPassword,
        new_password_confirm: this.retypePassword,
      };
      await this.$http.post("/accounts/change", form);
      this.$notify("success", "Your password has been changed.");
    },
  },
};
</script>

<style lang="scss" scoped></style>
