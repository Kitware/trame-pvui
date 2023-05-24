<template>
  <v-col fluid style="position: relative" v-show="shouldShow">
    <div style="position: absolute; right: 10px; top: -1px; z-index: 1">
      <v-btn v-if="help" icon x-small @click="showHelp = !showHelp">
        <v-icon small>mdi-lifebuoy</v-icon>
      </v-btn>
    </div>

    <v-row>
      <v-col v-if="label" class="py-0">
        <div class="text-caption text--secondary">{{ label }}</div>
        <v-divider />
        <div v-if="help && showHelp" class="text-caption text--secondary">
          {{ help }}
        </div>
      </v-col>
    </v-row>
    <v-color-picker
      class="mt-4"
      v-model="model"
      hide-mode-switch
      canvas-height="45"
    />
  </v-col>
</template>

<script>
import { floatToHex2, debounce, areEquals, shouldShowDecorator } from './utils';

export default {
  name: 'swColorSelector',
  props: {
    name: {
      type: String,
    },
    size: {
      type: Number,
      default: 1,
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
    type: {
      type: String,
    },
    initial: {},
  },
  data() {
    return {
      color: '#ffffff',
      showHelp: false,
      query: '',
    };
  },
  created() {
    this.flushToServer = debounce(() => {
      const value = (this.properties() && this.properties()[this.name]) || [];
      if (!areEquals(this.initial, value)) {
        this.dirty(this.name);
      }
    }, 100);
    this.onQuery = (query) => {
      this.query = query;
    };
    this.simputChannel.$on('query', this.onQuery);
  },
  beforeDestroy() {
    this.simputChannel.$off('query', this.onQuery);
  },
  computed: {
    shouldShow: shouldShowDecorator,
    model: {
      get() {
        /* eslint-disable no-unused-expressions */
        this.mtime; // force refresh
        const value = this.properties() && this.properties()[this.name];
        if (!value) {
          return '#FFFFFF';
        }
        return `#${floatToHex2(value[0])}${floatToHex2(value[1])}${floatToHex2(
          value[2]
        )}`;
      },
      set(hexStr) {
        this.properties()[this.name] = [
          parseInt(hexStr.substr(1, 2), 16) / 255,
          parseInt(hexStr.substr(3, 2), 16) / 255,
          parseInt(hexStr.substr(5, 2), 16) / 255,
        ];
        this.flushToServer();
      },
    },
    decorator() {
      /* eslint-disable no-unused-expressions */
      this.mtime; // force refresh
      return (
        this.domains()[this.name]?.decorator?.available || {
          show: true,
          enable: true,
          query: true,
        }
      );
    },
    hints() {
      /* eslint-disable no-unused-expressions */
      this.mtime; // force refresh
      return this.domains()?.[this.name]?.hints || [];
    },
  },
  inject: [
    'simputChannel',
    'data',
    'properties',
    'domains',
    'dirty',
    'getSimput',
  ],
};
</script>
