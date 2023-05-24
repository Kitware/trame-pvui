<template>
  <v-switch
    class="py-0 mt-0"
    v-model="model"
    @change="validate"
    dense
    hide-details
  />
</template>

<script>
export default {
  name: 'swNestedSwitch',
  props: {
    name: {
      type: String,
    },
    mtime: {
      type: Number,
    },
  },
  computed: {
    model: {
      get() {
        /* eslint-disable no-unused-expressions */
        this.mtime; // force refresh
        return (this.properties() && this.properties()[this.name]) || false;
      },
      set(v) {
        this.properties()[this.name] = v ? 1 : 0;
      },
    },
  },
  methods: {
    validate() {
      this.dirty(this.name);
    },
  },
  inject: ['data', 'properties', 'dirty'],
};
</script>
