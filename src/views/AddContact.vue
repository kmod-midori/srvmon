<template>
  <div>
    <v-form>
      <v-row>
        <v-col>
          <v-text-field
            v-model="label"
            label="Label"
            required
            :error-messages="labelErrors"
            @input="$v.label.$touch()"
            @blur="$v.label.$touch()"
          ></v-text-field>
        </v-col>
      </v-row>

      <v-row>
        <!-- Mode Selector -->
        <v-col sm="12" md="6">
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
      </v-row>
      <!-- Mode Specific -->
      <v-col class="py-0">
        <v-row>
          <template v-if="mode == 0"></template>
          <template v-else-if="mode == 1"></template>
        </v-row>
      </v-col>
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
import {
  required,
  integer,
  between,
  minValue,
  helpers,
  email,
} from "vuelidate/lib/validators";
import { isWebUri } from "valid-url";

export default {
  mixins: [validationMixin],
  validations() {
    const v = {
      label: {
        required,
      },
    };

    return v;
  },

  data() {
    return {
      label: "",
      mode: 0,
      modes: [
        {
          key: "email",
          title: "E-mail",
        },
        {
          key: "webhook",
          title: "Webhook",
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
  },

  methods: {
    submit() {},
  },
};
</script>
