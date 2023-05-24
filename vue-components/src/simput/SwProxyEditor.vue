<template>
  <v-card
    outlined
    tile
    class="px-0"
    v-show="decorator.show"
    style="position: relative"
  >
    <v-card-title class="py-1 px-0">
      <v-btn icon @click="toggleCollapse">
        <v-icon>{{ collapseIcon }}</v-icon>
      </v-btn>
      {{ label }}
      <v-spacer />
      <SimputItem no-ui :itemId="itemId">
        <template v-slot="{ data }">
          <sw-nested-switch :name="togglePropertyName" :mtime="data.mtime" />
        </template>
      </SimputItem>
    </v-card-title>
    <v-divider v-if="!collapsed" />
    <v-card-text v-show="!collapsed" class="px-0 my-n4">
      <SimputItem :itemId="itemId" />
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'swProxyEditor',
  props: {
    name: {
      type: String,
    },
    label: {
      type: String,
    },
    help: {
      type: String,
    },
    mtime: {
      type: Number,
    },
    hints: {
      type: String,
    },
  },
  data() {
    return {
      collapsed: true,
    };
  },
  computed: {
    decorator() {
      /* eslint-disable no-unused-expressions */
      this.mtime; // force refresh
      return this.domains()[this.name]?.decorator?.available || { show: true };
    },
    collapseIcon() {
      return this.collapsed ? 'mdi-chevron-right' : 'mdi-chevron-down';
    },
    parentId() {
      /* eslint-disable no-unused-expressions */
      this.mtime; // force refresh
      return this.data().id;
    },
    itemId() {
      /* eslint-disable no-unused-expressions */
      this.mtime; // force refresh
      return this.properties()[this.name];
    },
    togglePropertyName() {
      if (this.hints) {
        const list = JSON.parse(atob(this.hints)).children;
        const toggleProp = list.find(
          ({ elem_name }) => elem_name === 'ProxyEditorPropertyWidget'
        );
        if (toggleProp) {
          return toggleProp.property;
        }
      }
      return false;
    },
  },
  methods: {
    toggleCollapse() {
      this.collapsed = !this.collapsed;
    },
  },
  inject: ['data', 'domains', 'properties'],
};
</script>
