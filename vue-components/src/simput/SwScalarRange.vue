<template>
  <v-card outlined tile class="px-0 mt-n2" v-show="decorator.show">
    <v-card-title class="py-1 px-1">
      <v-btn small icon @click="resetToDefault">
        <v-icon>mdi-home-circle-outline</v-icon>
      </v-btn>
      <v-btn
        small
        icon
        @click="toggleRange"
        :disabled="!availableScalarRange"
        :color="showValueGenerator ? 'primary' : ''"
      >
        <v-icon small>mdi-arrow-expand-horizontal</v-icon>
      </v-btn>
      <v-col class="py-0 my-0">
        <div v-if="!availableScalarRange">{{ label }}</div>
        <v-row v-if="availableScalarRange" class="text-caption py-0 my-0">
          <v-col cols="6" class="text-truncate py-0 my-0">
            {{ availableScalarRange[0] }}
          </v-col>
          <v-col cols="6" class="text-truncate py-0 my-0">
            {{ availableScalarRange[1] }}
          </v-col>
        </v-row>
      </v-col>

      <v-btn small icon @click="clearEntries">
        <v-icon>mdi-close-circle-outline</v-icon>
      </v-btn>
      <v-btn small icon @click="addEntry">
        <v-icon>mdi-plus-circle-outline</v-icon>
      </v-btn>
    </v-card-title>
    <v-divider v-if="availableScalarRange && showValueGenerator" />
    <v-row
      v-if="availableScalarRange && showValueGenerator"
      class="px-2 py-0 my-0"
      align="center"
    >
      <v-col cols="4">
        <v-text-field
          label="Min"
          v-model="minValue"
          type="number"
          dense
          hide-details
        />
      </v-col>
      <v-col cols="4">
        <v-text-field
          label="Max"
          v-model="maxValue"
          type="number"
          dense
          hide-details
        />
      </v-col>
      <v-col cols="4">
        <v-row>
          <v-text-field
            label="Count"
            v-model="spreadCount"
            type="number"
            min="3"
            max="1000"
            step="1"
            @input="spreadValues"
            dense
            hide-details
          />
          <v-btn small icon @click="spreadValues" color="green" class="mx-2">
            <v-icon>mdi-check-circle-outline</v-icon>
          </v-btn>
        </v-row>
      </v-col>
    </v-row>
    <v-divider />
    <v-card-text>
      <v-col class="pa-0">
        <v-row v-for="(v, i) in model" :key="i" align="center">
          <v-text-field
            v-model="model[i]"
            hide-details
            dense
            @blur="validate"
            class="px-2 my-0 py-0"
          />
          <v-btn small icon @click="removeEntry(i)">
            <v-icon>mdi-minus-circle-outline</v-icon>
          </v-btn>
        </v-row>
      </v-col>
    </v-card-text>
  </v-card>
</template>

<script>
export default {
  name: 'swScalarRange',
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
    size: {
      type: Number,
    },
    hints: {
      type: String,
    },
  },
  data() {
    return {
      spreadCount: 10,
      minValue: 0,
      maxValue: 0,
      showValueGenerator: false,
    };
  },
  computed: {
    model: {
      get() {
        /* eslint-disable no-unused-expressions */
        this.mtime; // force refresh
        const value = this.properties() && this.properties()[this.name];
        if (!value) {
          return [];
        }
        if (Array.isArray(value)) {
          return value;
        }
        return [value];
      },
      set(array) {
        this.properties()[this.name] = array; // array.map(Number);
      },
    },
    decorator() {
      /* eslint-disable no-unused-expressions */
      this.mtime; // force refresh
      return (
        this.domains()[this.name]?.decorator?.available || {
          show: true,
          query: true,
        }
      );
    },
    availableScalarRange() {
      return this.domains()[this.name]?.scalar_range?.available;
    },
  },
  watch: {
    availableScalarRange(range) {
      if (range && range[0] !== this.minValue) {
        this.minValue = range[0];
      }
      if (range && range[1] !== this.maxValue) {
        this.maxValue = range[1];
      }
    },
  },
  methods: {
    toggleRange() {
      this.showValueGenerator = !this.showValueGenerator;
    },
    addEntry() {
      let nextValue = 0;
      if (this.model.length > 1) {
        const [a, b] = this.model.slice(-2);
        const delta = b - a;
        nextValue = b + delta;
      }
      this.model = [].concat(this.model, nextValue);
      this.dirty(this.name);
    },
    removeEntry(index = -1) {
      if (index === -1) {
        this.model = this.model.slice(0, -1);
      } else {
        this.model = this.model.filter((v, i) => i !== index);
      }

      this.dirty(this.name);
    },
    clearEntries() {
      this.model = [];
      this.dirty(this.name);
    },
    resetToDefault() {
      if (this.availableScalarRange) {
        this.model = [
          0.5 * (this.availableScalarRange[0] + this.availableScalarRange[1]),
        ];
        this.dirty(this.name);
        this.resetRange();
      }
    },
    spreadValues() {
      const min = Number(this.minValue);
      const max = Number(this.maxValue);
      const count = Number(this.spreadCount);
      const delta = (max - min) / (count - 1);
      const values = [];
      let currentValue = min;
      while (values.length < count) {
        values.push(currentValue);
        currentValue += delta;
      }
      this.model = values;
      this.dirty(this.name);
    },
    validate() {
      this.model = this.model.map(Number);
      this.dirty(this.name);
    },
    resetRange() {
      const dataRange = this.availableScalarRange || [0, 1];
      this.minValue = dataRange[0];
      this.maxValue = dataRange[1];
    },
  },
  inject: ['data', 'domains', 'properties', 'dirty'],
};
</script>
