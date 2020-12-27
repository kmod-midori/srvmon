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
                <v-list-item
                  v-for="item in modes"
                  :key="item.key"
                  :disabled="item.disabled"
                >
                  <v-list-item-content>
                    <v-list-item-title v-text="item.title"></v-list-item-title>
                    <v-list-item-subtitle
                      v-text="item.desc"
                    ></v-list-item-subtitle>
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
              <v-col sm="12" md="8">
                <v-text-field
                  v-model="url"
                  label="URL"
                  required
                  :error-messages="urlErrors"
                  @input="$v.url.$touch()"
                  @blur="$v.url.$touch()"
                ></v-text-field>
              </v-col>
              <v-col sm="12" md="4">
                <v-combobox
                  v-model="validStatus"
                  :items="statuses"
                  label="Valid status codes"
                  multiple
                  :error-messages="validStatusErrors"
                  @input="$v.validStatus.$touch()"
                  @blur="$v.validStatus.$touch()"
                ></v-combobox>
              </v-col>
            </template>

            <template v-else-if="mode == 1">
              <v-col>
                <v-text-field
                  v-model="address"
                  label="Address"
                  hint="IP address or domain name"
                  required
                  :error-messages="addressErrors"
                  @input="$v.address.$touch()"
                  @blur="$v.address.$touch()"
                ></v-text-field>
              </v-col>
              <v-col cols="2">
                <v-text-field
                  v-model="port"
                  label="Port"
                  required
                  :error-messages="portErrors"
                  @input="$v.port.$touch()"
                  @blur="$v.port.$touch()"
                ></v-text-field>
              </v-col>
            </template>

            <template v-else-if="mode == 2">
              <v-col>
                <v-alert text prominent type="info" icon="mdi-information">
                  No special settings needed
                </v-alert>
              </v-col>
            </template>
          </v-row>
        </v-col>
      </v-row>
      <v-row>
        <!-- Timeout -->
        <v-col sm="12" md="4" v-if="mode !== 2">
          <v-text-field
            v-model="timeout"
            label="Timeout (ms)"
            required
            :error-messages="timeoutErrors"
            @input="$v.timeout.$touch()"
            @blur="$v.timeout.$touch()"
          ></v-text-field>
        </v-col>
        <!-- Interval -->
        <v-col sm="12" md="4">
          <v-text-field
            v-model="interval"
            label="Interval (seconds)"
            required
            :error-messages="intervalErrors"
            @input="$v.interval.$touch()"
            @blur="$v.interval.$touch()"
          ></v-text-field>
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
import {
  required,
  integer,
  between,
  minValue,
  helpers,
} from "vuelidate/lib/validators";
import { isWebUri } from "valid-url";

const url = (value) => !helpers.req(value) || !!isWebUri(value);

export default {
  mixins: [validationMixin],
  validations() {
    const timeV = {
      required,
      integer,
      minValue: minValue(1),
    };

    const v = {
      label: {
        required,
      },
      interval: timeV,
    };

    if (this.mode === 0) {
      v.url = { url, required };
      v.validStatus = {
        required,
        $each: {
          integer,
          between: between(100, 599),
        },
      };
      v.timeout = timeV;
    } else if (this.mode === 1) {
      v.port = { required, integer, between: between(1, 65535) };
      v.address = { required };
      v.timeout = timeV;
    }

    return v;
  },
  data() {
    return {
      editId: null,
      label: "New Server",
      mode: 0,
      timeout: 3000,
      interval: 300,
      url: "",
      address: "",
      port: 22,
      modes: [
        {
          key: "active-http",
          title: "Active HTTP",
          desc:
            "A HTTP request will be sent to the specified URL periodically.",
        },
        {
          key: "active-tcp",
          title: "Active TCP",
          desc: "A TCP handshake will be done periodically.",
        },
        {
          key: "passive-http",
          title: "Passive HTTP (coming soon)",
          desc:
            "Your server will make a HTTP request to a URL that will be generated.",
          disabled: true,
        },
      ],
      statuses: [
        "200",
        "201",
        "202",
        "203",
        "204",
        "205",
        "206",
        "301",
        "302",
        "303",
        "304",
        "305",
        "306",
        "307",
        "308",
        "401",
        "402",
        "403",
        "404",
        "405",
      ],
      validStatus: ["200", "204"],
    };
  },
  mounted() {
    if (this.$route.params.id) {
      this.editId = parseInt(this.$route.params.id, 10);
      this.$http.get(`/servers/${this.editId}`).then((resp) => {
        const server = resp.data.payload;
        this.label = server.label;
        this.interval = server.config.interval;
        switch (server.mode) {
          case "active-http":
            this.mode = 0;
            this.timeout = server.config.timeout;
            this.url = server.config.url;
            this.validStatus = server.config.validStatus.map((s) =>
              s.toString()
            );
            break;
          case "active-tcp":
            this.mode = 1;
            this.address = server.config.address;
            this.port = server.config.port;
            this.timeout = server.config.timeout;
            break;
          case "passive-http":
            this.mode = 2;
            break;
        }
      });
    }
  },
  computed: {
    timeoutLabel() {
      let ret = "";
      switch (this.mode) {
        case 0:
        case 1:
          ret = "Interval";
          break;
        case 2:
          ret = "Timeout";
          break;
      }
      return ret + " (seconds)";
    },
    labelErrors() {
      const errors = [];
      if (!this.$v.label.$dirty) return errors;
      !this.$v.label.required && errors.push("Label is required");
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
    addressErrors() {
      const errors = [];
      if (!this.$v.address.$dirty) return errors;
      !this.$v.address.required && errors.push("Address is required");
      return errors;
    },
    portErrors() {
      const errors = [];
      const v = this.$v.port;
      if (!v.$dirty) return errors;
      !v.required && errors.push("Port is required");
      !v.integer && errors.push("Port must be an integer");
      !v.between && errors.push("Port must be 1-65535");
      return errors;
    },
    timeoutErrors() {
      const errors = [];
      const v = this.$v.timeout;
      if (!v.$dirty) return errors;
      !v.required && errors.push("Timeout is required");
      !v.integer && errors.push("Timeout must be an integer");
      !v.minValue && errors.push("Timeout must be greater then 1");
      return errors;
    },
    intervalErrors() {
      const errors = [];
      const v = this.$v.interval;
      if (!v.$dirty) return errors;
      !v.required && errors.push("Interval is required");
      !v.integer && errors.push("Interval must be an integer");
      !v.minValue && errors.push("Interval must be greater then 1");
      return errors;
    },
    validStatusErrors() {
      const errors = [];
      const v = this.$v.validStatus;
      if (!v.$dirty) return errors;
      !v.required && errors.push("At least one status code is required");
      v.$invalid && errors.push("Invalid status code");
      return errors;
    },
  },
  methods: {
    async submit() {
      const server = {
        label: this.label,
        mode: this.modes[this.mode].key,
        config: {},
      };

      switch (this.mode) {
        case 0:
          server.config = {
            url: this.url,
            validStatus: this.validStatus.map((status) => parseInt(status, 10)),
            timeout: parseInt(this.timeout, 10),
            interval: parseInt(this.interval, 10),
          };
          break;
        case 1:
          server.config = {
            address: this.address,
            port: parseInt(this.port, 10),
            timeout: parseInt(this.timeout, 10),
            interval: parseInt(this.interval, 10),
          };
          break;
        case 2:
          server.config = {
            interval: parseInt(this.interval, 10),
          };
          break;
        default:
          break;
      }

      if (this.editId) {
        await this.$http.post(`/servers/${this.editId}`, server);
        this.$notify("success", "Changes saved.");
      } else {
        await this.$http.put("/servers", server);
        this.$notify("success", "Server added.");
      }

      this.$router.back();
    },
  },
};
</script>
