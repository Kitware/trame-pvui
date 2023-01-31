<script lang="ts">
import { HistogramData } from '../../utils/types';
export default {
  props: {
    targets: {
      type: Array,
      required: true,
    },
    container: {
      type: HTMLElement,
      required: true,
    },
    histogramData: {
      type: Object as () => HistogramData,
      required: true,
    },
    nodes: {
      type: Array,
      required: true,
    },
    positionToScalar: {
      type: Function,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      show: false,
      targetValue: undefined,
      binInfo: undefined,
    };
  },
  computed: {
    numBins() {
      return this.histogramData.counts.length;
    },
    binSize() {
      return (
        (this.histogramData.range[1] - this.histogramData.range[0]) /
        this.numBins
      );
    },
    bins() {
      const bins = [];
      for (var i = 0; i < this.numBins; i++) {
        const lower = Math.round(
          this.histogramData.range[0] + this.binSize * i
        );
        const upper = Math.round(
          this.histogramData.range[0] + this.binSize * (i + 1)
        );
        bins.push([lower, upper]);
      }
      return bins;
    },
  },
  methods: {
    moveTooltip(e) {
      if (this.targets.includes(e.target)) {
        this.show = true;
        this.$nextTick(() => {
          if (this.$refs.tooltip) {
            const left = e.pageX - this.container.offsetLeft + 5;
            const top = e.pageY - this.container.offsetTop + 5;
            this.$refs.tooltip.$el.style.left = left + 'px';
            this.$refs.tooltip.$el.style.top = top + 'px';
            this.targetValue = Math.round(this.positionToScalar(left - 20));
          }
          if (e.target.className.includes('histogram-canvas')) {
            const proportion =
              (this.targetValue - this.histogramData.range[0]) /
              (this.histogramData.range[1] - this.histogramData.range[0]);
            const binNumber = Math.floor(this.numBins * proportion);
            this.binInfo = {
              number: binNumber,
              count: this.histogramData.counts[binNumber],
              range: this.bins[binNumber],
            };
          } else {
            this.binInfo = undefined;
          }
        });
      } else {
        this.show = false;
        this.targetValue = undefined;
        this.binInfo = undefined;
      }
    },
    getColorSquare(targetValue) {
      let leftNode = undefined;
      let rightNode = undefined;
      let newRGBString = 'rgb(0, 0, 0)';

      this.nodes.forEach((node) => {
        if (node[0] <= targetValue) {
          if (!leftNode || node[0] > leftNode[0]) {
            leftNode = node;
          }
        } else {
          if (!rightNode || node[0] < rightNode[0]) {
            rightNode = node;
          }
        }
      });
      if (!leftNode) {
        newRGBString = `rgb(${rightNode[1] * 255}, ${rightNode[2] * 255}, ${
          rightNode[3] * 255
        })`;
      } else if (!rightNode) {
        newRGBString = `rgb(${leftNode[1] * 255}, ${leftNode[2] * 255}, ${
          leftNode[3] * 255
        })`;
      } else {
        const proportion =
          (targetValue - leftNode[0]) / (rightNode[0] - leftNode[0]);
        const newRGB = leftNode.slice(1).map((v, i) => {
          return Math.round(((rightNode[i + 1] - v) * proportion + v) * 255);
        });
        newRGBString = `rgb(${newRGB[0]}, ${newRGB[1]}, ${newRGB[2]})`;
      }
      return `margin-left: 5px; background-color: ${newRGBString}`;
    },
  },
  mounted() {
    document.addEventListener('mousemove', this.moveTooltip, false);
  },
};
</script>

<template>
  <v-card v-show="show" ref="tooltip" :dark="dark" class="mouse-tooltip pa-2">
    <div v-if="targetValue">
      Value = {{ targetValue }}
      <div
        v-if="!binInfo"
        class="color-square"
        :style="getColorSquare(targetValue)"
      ></div>
    </div>
    <div v-if="binInfo && binInfo.range" class="caption">
      Bin range: {{ binInfo.range[0] }}...{{ binInfo.range[1] }}
    </div>
    <div v-if="binInfo" class="caption">Bin count: {{ binInfo.count }}</div>
  </v-card>
</template>

<style scoped>
.mouse-tooltip {
  width: fit-content;
  position: absolute;
  z-index: 4;
}
</style>
