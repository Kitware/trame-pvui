<script lang="ts">
import { HistogramData } from '../../utils/types';
import { makeDraggable } from '../../utils/drag';

export default {
  props: {
    index: {
      type: Number,
      required: true,
    },
    scalarValue: {
      type: Number,
      required: true,
    },
    rgbValue: {
      type: Array,
      required: true,
    },
    histogramData: {
      type: Object as () => HistogramData,
      required: true,
    },
    colorLine: {
      required: true,
    },
    dataRange: {
      type: Array,
      required: true,
    },
    visibleColorPicker: {
      type: Number || undefined,
      default: undefined,
    },
    scalarToPosition: {
      type: Function,
      required: true,
    },
    positionToScalar: {
      type: Function,
      required: true,
    },
    dark: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      xPosition: 0,
    };
  },
  computed: {
    rgbString() {
      const rgb = this.rgbValue.map((value) => value * 255);
      return `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]})`;
    },
  },
  methods: {
    onDragSquare() {
      const scalar = Math.round(this.positionToScalar(this.$el.offsetLeft));
      const newValue = [scalar, ...this.rgbValue];
      this.$emit('change', this.index, newValue);
    },
    updateXPosition() {
      if (!this.colorLine) return;
      this.xPosition = this.scalarToPosition(this.scalarValue);
    },
    toggleColorPicker(index) {
      if (this.visibleColorPicker !== index) {
        this.$emit('pick', index);
      } else {
        this.$emit('pick', undefined);
      }
    },
  },
  mounted() {
    this.updateXPosition();
  },
  updated() {
    this.updateXPosition();

    makeDraggable(
      this.$el,
      this.onDragSquare,
      {
        x: [-10, this.colorLine.clientWidth - 10],
        y: [],
      },
      {
        x: this.dataRange.map((value) => this.scalarToPosition(value)),
        y: [],
      }
    );
  },
};
</script>

<template>
  <div
    ref="colorSquare"
    v-if="colorLine"
    :class="!dark ? 'color-square' : 'color-square dark'"
    :style="`left: ${xPosition}px; background-color: ${rgbString}`"
    @dblclick="() => toggleColorPicker(index)"
  />
</template>

<style scoped>
.color-square {
  position: absolute;
  top: 0px;
  margin-top: 10px;
  height: 20px;
  width: 20px;
  border: 3px solid black;
}
.color-square.dark {
  border: 3px solid white;
}
.color-square::after {
  content: '\25B2';
  font-size: 16px;
  position: relative;
  top: -20px;
}
</style>
