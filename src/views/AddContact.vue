<template>
  <div>
    <v-form @submit.prevent="submit">
      <v-row>
        <!-- Mode Selector -->
        <v-col cols="12" md="6">
          <v-card>
            <v-list>
              <v-list-item-group v-model="mode" mandatory>
                <v-list-item v-for="item in modes" :key="item.key">
                  <v-list-item-content>
                    <v-list-item-title>{{ item.title }}</v-list-item-title>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card>
        </v-col>
        <!-- Mode Specific -->
        <v-col class="py-0">
          <v-row>
            <template v-if="mode == 0">
              <v-col>
                <v-text-field
                  type="email"
                  v-model="address"
                  label="Address"
                  required
                  :error-messages="addressErrors"
                  @input="$v.address.$touch()"
                  @blur="$v.address.$touch()"
                ></v-text-field>
              </v-col>
            </template>

            <template v-else-if="mode == 1">
              <v-col cols="12" md="4">
                <v-select
                  v-model="service"
                  label="Service"
                  :items="services"
                  item-text="name"
                  item-value="value"
                ></v-select>
              </v-col>
              <v-col cols="12" md="8">
                <v-text-field
                  v-model="url"
                  label="URL"
                  required
                  :error-messages="urlErrors"
                  @input="$v.url.$touch()"
                  @blur="$v.url.$touch()"
                ></v-text-field>
              </v-col>
            </template>
          </v-row>
        </v-col>
      </v-row>
    </v-form>

    <v-fab-transition>
      <v-btn
        fab
        fixed
        bottom
        right
        :disabled="$v.$invalid"
        color="success"
        @click="submit"
      >
        <v-icon>mdi-content-save</v-icon>
      </v-btn>
    </v-fab-transition>
  </div>
</template>

<script>
import { validationMixin } from "vuelidate";
import { required, helpers, email } from "vuelidate/lib/validators";
import { isWebUri } from "valid-url";
const url = (value) => !helpers.req(value) || !!isWebUri(value);
export default {
  mixins: [validationMixin],
  validations() {
    const v = {};

    if (this.mode === 0) {
      v.address = { required, email };
    } else if (this.mode === 1) {
      v.url = { required, url };
    }

    return v;
  },

  data() {
    return {
      mode: 0,
      modes: [
        {
          key: "email",
          title: "Email",
        },
        {
          key: "webhook",
          title: "Webhook",
        },
      ],
      address: "",
      url: "",
      service: "ding",
      services: [
        {
          name: "DingTalk",
          value: "ding",
        },
        {
          name: "Discord",
          value: "discord",
        },
      ],
    };
  },

  computed: {
    labelErrors() {
      const errors = [];
      if (!this.$v.label.$dirty) return errors;
      !this.$v.label.required && errors.push("Label is required");
      return errors;
    },
    addressErrors() {
      const errors = [];
      if (!this.$v.address.$dirty) return errors;
      !this.$v.address.required && errors.push("Address is required");
      !this.$v.address.email && errors.push("Invalid email address");
      return errors;
    },
    urlErrors() {
      const errors = [];
      const v = this.$v.url;
      if (!v.$dirty) return errors;
      !v.required && errors.push("URL is required");
      !v.url && errors.push("Invalid URL");
      return errors;
    },
  },

  methods: {
    async submit() {
      if (this.$v.$invalid) return;
      const contact = {
        type: this.modes[this.mode].key,
      };
      switch (this.mode) {
        case 0:
          // email
          contact.config = {
            address: this.address,
          };
          break;
        case 1:
          // webhook
          contact.config = {
            service: this.service,
            url: this.url,
          };
          break;
      }

      await this.$http.put("/contacts", contact);
      this.$notify("success", "Contact added.");
      this.$router.back();
    },
  },
};
</script>
