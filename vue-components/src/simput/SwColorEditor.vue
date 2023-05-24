<template>
  <v-col class="px-0" v-show="shouldShowTextToQuery">
    <div class="text-h6 px-2">{{ label }}</div>
    <v-divider class="pt-0 mt-0" />
    <v-row class="mx-0 px-1 py-3">
      <v-col class="py-0">
        <v-select
          :key="tsKey"
          v-model="colorMode"
          :items="colorOptions"
          hide-details
          dense
        />
      </v-col>
      <v-col class="py-0" v-if="componentOptions">
        <v-select
          :key="tsKey"
          v-model="componentMode"
          :items="componentOptions"
          hide-details
          dense
        />
      </v-col>
    </v-row>

    <v-row class="mx-0 px-2 pt-1 mb-n6" v-show="colorMode === 'Solid Color'">
      <v-color-picker
        style="width: 100%"
        v-model="solidColor"
        hide-mode-switch
        canvas-height="50"
      />
    </v-row>

    <v-row
      class="mx-0 px-2 pt-1 justify-space-around mb-n6"
      v-show="colorMode !== 'Solid Color'"
    >
      <v-btn
        style="min-width: 36px"
        small
        class="mb-3 mx-1"
        :depressed="scalarBarVisible"
        :color="scalarBarVisible ? 'primary' : ''"
        @click="trigger('pv_reaction_representation_scalarbar_toggle')"
      >
        <v-icon small v-text="`$pqScalarBar`" />
      </v-btn>
      <v-btn
        style="min-width: 36px"
        small
        class="mb-3 mx-1"
        :depressed="useSeparateColorMap"
        :color="useSeparateColorMap ? 'primary' : ''"
        @click="useSeparateColorMap = !useSeparateColorMap"
      >
        <v-icon small v-text="`$pqSeparateColorMap`" />
      </v-btn>
      <v-spacer />
      <v-btn
        style="min-width: 36px"
        small
        class="mb-3 mx-1"
        @click="trigger('pv_reaction_scalar_range_data')"
      >
        <v-icon small v-text="`$pqResetRange`" />
      </v-btn>

      <v-btn
        style="min-width: 36px"
        small
        class="mb-3 mx-1"
        @click="trigger('pv_reaction_scalar_range_time')"
      >
        <v-icon small v-text="`$pqResetRangeTemporal`" />
      </v-btn>
    </v-row>
    <v-row class="mx-0 px-2 py-3" v-show="colorMode !== 'Solid Color'">
      <v-btn-toggle v-model="editingMode">
        <v-btn small value="edit_colormap">
          <v-icon small v-text="`$pqEditColor`" />
          Edit
        </v-btn>
        <v-btn style="min-width: 36px" small value="edit_scalar_range">
          <v-icon small v-text="`$pqResetRangeCustom`" />
        </v-btn>
        <v-btn style="min-width: 36px" small value="edit_presets">
          <v-icon small v-text="`$pqFavorites`" />
        </v-btn>
        <v-btn
          style="position: relative; min-width: 36px"
          small
          value="edit_scalarbar"
        >
          <v-icon small v-text="`$pqScalarBar`" />
          <div
            style="
              position: absolute;
              left: calc(50% + 5px);
              top: calc(50% + 5px);
              transform: translate(-50%, -50%);
            "
            class="text-caption font-weight-black text-lowercase"
          >
            e
          </div>
        </v-btn>
      </v-btn-toggle>
    </v-row>
    <v-row
      v-show="editingMode == 'edit_colormap'"
      class="mx-0 px-2 pt-1 justify-space-around"
    >
      Color map editing... TODO
    </v-row>
    <v-row
      v-show="editingMode == 'edit_scalar_range'"
      class="mx-0 px-2 pt-1 justify-space-around"
    >
      Custom data range editing... TODO
    </v-row>
    <v-row
      v-show="editingMode == 'edit_presets'"
      class="mx-0 px-2 pt-1 justify-space-around"
    >
      Color preset selection... TODO
    </v-row>
    <v-row
      v-show="editingMode == 'edit_scalarbar'"
      class="mx-0 px-2 pt-1 justify-space-around"
    >
      Scalar bar editing... TODO
    </v-row>
  </v-col>
</template>

<script>
import {
  floatToHex2,
  debounce,
  areEquals,
  shouldShowTextToQuery,
} from './utils';

let COUNT = 1;

// Nested properties:
// => AmbientColor, ColorArrayName, DiffuseColor, LookupTable, UseSeparateColorMap
export default {
  name: 'swColorEditor',
  props: {
    label: {
      type: String,
      default: 'Coloring',
    },
    mtime: {
      type: Number,
    },
  },
  created() {
    this.onUpdateUI = () => {
      const newValue = `__ColorEditor_${COUNT}__${this.uiTS()}`;
      if (this.tsKey !== newValue) {
        this.$nextTick(() => {
          this.tsKey = newValue;
        });
      }
    };
    this.simputChannel.$on('templateTS', this.onUpdateUI);
    this.flushSolidColorToServer = debounce(() => {
      // May have an issue for being 2 calls instead of just 1!
      this.dirtyMany('AmbientColor', 'DiffuseColor');
    }, 100);
    this.onQuery = (query) => {
      this.query = query;
    };
    this.simputChannel.$on('query', this.onQuery);
  },
  mounted() {
    COUNT++;
    this.onUpdateUI();
  },
  beforeDestroy() {
    this.simputChannel.$off('templateTS', this.onUpdateUI);
    this.simputChannel.$off('query', this.onQuery);
  },
  data() {
    return {
      tsKey: '__default__',
      componentMode: 'Magnitude',
      editingMode: null,
      query: '',
    };
  },
  watch: {
    componentMode() {
      this.updateColorBy();
    },
  },
  computed: {
    textToQuery() {
      return `${this.label} ${this.colorMode}`.toLowerCase();
    },
    shouldShowTextToQuery,
    scalarBarVisible() {
      return this.trame.state.get('active_representation_scalarbar_visibility');
    },
    arrayMap() {
      this.mtime; // force refresh
      const arrayMap = { 'Solid Color': { value: ['', '', '', '0', ''] } };
      const list = this.domains()?.ColorArrayName?.array_list?.available || [];
      for (let i = 0; i < list.length; i++) {
        const { text, value, components } = list[i];
        arrayMap[text] = { value, components };
      }
      return arrayMap;
    },
    componentOptions() {
      return this.arrayMap[this.colorMode]?.components;
    },
    colorOptions() {
      this.mtime; // force refresh
      const list = this.domains()?.ColorArrayName?.array_list?.available || [];
      const names = list.map(({ text }) => text);
      return ['Solid Color', ...names];
    },
    colorMode: {
      get() {
        this.mtime; // force refresh
        const fieldName = this.properties().ColorArrayName[4];
        if (fieldName.length) {
          return fieldName;
        }
        return 'Solid Color';
      },
      set(name) {
        this.properties().ColorArrayName = this.arrayMap[name]?.value;
        this.dirty('ColorArrayName');
        this.updateColorBy();
      },
    },
    solidColor: {
      get() {
        // AmbientColor, DiffuseColor
        const value = this.properties() && this.properties().AmbientColor;
        if (!value) {
          return '#FFFFFF';
        }
        return `#${floatToHex2(value[0])}${floatToHex2(value[1])}${floatToHex2(
          value[2]
        )}`;
      },
      set(hexStr) {
        const colorFloat = [
          parseInt(hexStr.substr(1, 2), 16) / 255,
          parseInt(hexStr.substr(3, 2), 16) / 255,
          parseInt(hexStr.substr(5, 2), 16) / 255,
        ];
        if (!areEquals(this.properties().AmbientColor, colorFloat)) {
          this.properties().AmbientColor = colorFloat;
          this.properties().DiffuseColor = colorFloat;
          this.flushSolidColorToServer();
        }
      },
    },
    useSeparateColorMap: {
      get() {
        return !!this.properties() && this.properties().UseSeparateColorMap;
      },
      set(v) {
        this.properties().UseSeparateColorMap = v ? 1 : 0;
        this.dirty('UseSeparateColorMap');
      },
    },
  },
  methods: {
    updateColorBy() {
      const field = this.properties().ColorArrayName;
      const name = field[4];
      const association = Number(field[3]);
      let component = this.componentOptions
        ? this.componentOptions.indexOf(this.componentMode)
        : -1;
      if (component !== -1) {
        component--;
      } else {
        this.componentMode = 'Magnitude';
      }

      if (name) {
        this.trigger('pv_reaction_representation_color_by', [
          [name, association, component],
        ]);
      } else {
        this.trigger('pv_reaction_representation_color_by');
      }
    },
  },
  inject: [
    'trame',
    'data',
    'properties',
    'domains',
    'dirty',
    'dirtyMany',
    'getSimput',
    'uiTS',
    'simputChannel',
    'trigger',
  ],
};
</script>
