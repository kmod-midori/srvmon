import Vue from "vue";

import { DateTime } from "luxon";

Vue.filter("luxon", function (val, fmt="yyyy-MM-dd HH:mm") {
  return DateTime.fromMillis(val).toFormat(fmt);
});
