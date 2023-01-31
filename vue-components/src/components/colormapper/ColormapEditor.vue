<script lang="ts">
import ColorNode from './ColorNode.vue';
import {
  drawHistogram,
  drawLabels,
  drawGradient,
} from '../../utils/canvasDrawing';
import { HistogramData } from '../../utils/types';
import ColorNodeList from './NodeList.vue';
import clamp from '../../utils/clamp';
import InfoTooltip from './InfoTooltip.vue';
import { listenDragSelection } from '../../utils/drag';
import OptionIcons from './OptionIcons.vue';
import OpacityEditor from './OpacityEditor.vue';

export default {
  components: {
    ColorNode,
    ColorNodeList,
    InfoTooltip,
    OptionIcons,
    OpacityEditor,
  },
  props: {
    colors: {
      type: Array,
      required: true,
    },
    opacities: {
      type: Array,
      required: true,
    },
    histogramData: {
      type: Object as () => HistogramData,
      required: true,
    },
    dark: {
      type: Boolean,
      required: false,
    },
  },
  computed: {
    computedDark() {
      return this.dark === undefined ? this.$vuetify.theme.dark : this.dark;
    },
    dataRange() {
      return this.histogramData.range;
    },
    gradientLength() {
      // -40 accounts for the 20px padding on either side
      return this.$refs.colorLine.clientWidth - 40;
    },
    rangeDifference() {
      return this.dataRange[1] - this.dataRange[0];
    },
  },
  data() {
    return {
      colorLine: undefined,
      colorNodes: this.colors,
      opacityNodes: this.opacities,
      selectedNodes: [],
      visibleColorPicker: undefined,
      filterRange: undefined,
      options: {
        opacityMode: false,
        showHistogram: false,
      },
    };
  },
  methods: {
    nodeToTableItem(node, index, opacity) {
      let rgb;
      if (!opacity) {
        rgb = node.slice(1).map((value) => value * 255);
        rgb = [...rgb, 1];
      } else {
        rgb = this.computedDark ? [255, 255, 255, node[1]] : [0, 0, 0, node[1]];
      }
      return {
        id: index,
        value: node[0],
        rgbString: `rgb(${rgb[0]}, ${rgb[1]}, ${rgb[2]}, ${rgb[3]})`,
        rgb,
        index,
      };
    },
    scalarToPosition(scalar) {
      let calculatedPosition =
        this.gradientLength *
        ((scalar - this.dataRange[0]) / this.rangeDifference);
      calculatedPosition = clamp(
        calculatedPosition,
        -20,
        this.gradientLength + 20
      );
      calculatedPosition += 10; // +10 accounts for half the square width
      return calculatedPosition;
    },
    positionToScalar(position) {
      position -= 10; // -10 accounts for half the square width
      return Math.round(
        (position / this.gradientLength) * this.rangeDifference +
          this.dataRange[0]
      );
    },
    getFullRange() {
      return [
        this.positionToScalar(this.scalarToPosition(this.dataRange[0]) - 20),
        this.positionToScalar(this.scalarToPosition(this.dataRange[1]) + 20),
      ].map((val) => Math.floor(val));
    },
    render() {
      this.colorLine = this.$refs.colorLine;
      if (this.options.showHistogram) {
        drawHistogram(
          this.histogramData,
          this.$refs.histogram,
          this.computedDark
        );
      }
      if (!this.options.opacityMode) {
        drawLabels(this.histogramData, this.$refs.histogramLabels);
      }
      drawGradient(
        this.colorNodes,
        this.$refs.gradientBox,
        this.getFullRange(),
        this.dataRange[0]
      );
    },
    createNodeAtClick(event) {
      const newNodeValue = Math.round(this.positionToScalar(event.layerX));
      const newNode = [newNodeValue, 0, 0, 0];
      this.colorNodes = [...this.colorNodes, newNode];
      this.selectedNodes = [
        this.nodeToTableItem(newNode, this.colorNodes.length - 1),
      ];
      this.render();
    },
    updateOption(optionName, newValue) {
      this.options[optionName] = newValue;
    },
    updateFilterRange(newRange) {
      this.filterRange = newRange;
    },
    updateSelectedNodes(selected) {
      this.selectedNodes = selected;
    },
    updateVisibleColorPicker(visibleColorPicker) {
      this.visibleColorPicker = visibleColorPicker;
    },
    updateSingleNode(nodeIndex, newValue) {
      this.colorNodes[nodeIndex] = newValue;
      this.colorNodes = [...this.colorNodes];
      this.render();
      this.$emit('updateColors', [...this.colorNodes]);
    },
    updateNodeList(newList) {
      this.colorNodes = newList;
      this.render();
      this.$emit('updateColors', [...this.colorNodes]);
    },
    updateOpacityNodes(newList) {
      this.opacityNodes = newList;
      this.$emit('updateOpacities', [...this.opacityNodes]);
    },
  },
  mounted() {
    listenDragSelection(
      this.$refs.histogramLabels,
      (startPos: number, endPos: number) => {
        const startValue = this.positionToScalar(startPos);
        const endValue = this.positionToScalar(endPos);
        this.filterRange = [startValue, endValue];
      }
    );
    this.render();
  },
  updated() {
    this.render();
  },
};
</script>

<template>
  <div
    ref="container"
    :class="!computedDark ? 'widget-container' : 'widget-container dark'"
  >
    <v-tooltip right>
      <template v-slot:activator="{ on, attrs }">
        <v-icon
          class="help-circle"
          :dark="computedDark"
          v-bind="attrs"
          v-on="on"
        >
          mdi-help-circle
        </v-icon>
      </template>
      <div class="caption" v-if="!options.opacityMode">
        Double click gradient bar to create new control point
        <br />
        Double click existing control point to edit color
        <br />
        Drag along section of gradient to select range and filter table
        <br />
        Drag existing control point to edit its value
      </div>
      <div class="caption" v-else>
        Drag a function node to move/select it
        <br />
        Drag a node's control points to edit the curve between two nodes
        <br />
        Click anywhere else on the graph to create a new node
        <br />
        Use the node list below to edit and delete points
      </div>
    </v-tooltip>
    <option-icons
      :options="options"
      :dark="computedDark"
      @update="updateOption"
    />
    <info-tooltip
      v-if="colorLine"
      :dark="computedDark"
      :container="$refs.container"
      :positionToScalar="positionToScalar"
      :histogramData="histogramData"
      :nodes="colorNodes"
      :targets="[$refs.histogram, $refs.histogramLabels, $refs.colorLine]"
    />
    <canvas
      v-if="options.showHistogram"
      ref="histogram"
      class="histogram-canvas indented"
    />
    <div v-else :class="options.opacityMode ? 'tall-gap' : ''" />
    <opacity-editor
      v-if="options.opacityMode"
      :opacityNodes="opacityNodes"
      :selectedNodes="selectedNodes"
      :dark="computedDark"
      :dataRange="dataRange"
      @update="updateOpacityNodes"
      @select="updateSelectedNodes"
    />
    <div
      ref="histogramLabels"
      :class="
        options.showHistogram || options.opacityMode
          ? 'histogram-labels shifted indented'
          : 'histogram-labels indented'
      "
      @dblclick="createNodeAtClick"
    />
    <div
      ref="colorLine"
      v-if="!options.opacityMode"
      :class="!computedDark ? 'color-line' : 'color-line dark'"
    >
      <canvas ref="gradientBox" class="gradient-box" />
      <color-node
        v-for="(node, index) in colorNodes"
        :key="'node_' + index"
        :index="index"
        :scalarValue="node[0]"
        :rgbValue="node.slice(1)"
        :histogramData="histogramData"
        :colorLine="colorLine"
        :dataRange="dataRange"
        :dark="computedDark"
        :visibleColorPicker="visibleColorPicker"
        :scalarToPosition="scalarToPosition"
        :positionToScalar="positionToScalar"
        @change="updateSingleNode"
        @pick="updateVisibleColorPicker"
        @updaterange="updateFilterRange"
      />
    </div>
    <color-node-list
      v-if="!options.opacityMode"
      :nodes="colorNodes"
      :selectedNodes="selectedNodes"
      :visibleColorPicker="visibleColorPicker"
      :nodeToTableItem="nodeToTableItem"
      :filterRange="filterRange"
      :dark="computedDark"
      @change="updateNodeList"
      @select="updateSelectedNodes"
      @pick="updateVisibleColorPicker"
    />
    <color-node-list
      v-else
      :opacityMode="options.opacityMode"
      :nodes="opacityNodes"
      :selectedNodes="selectedNodes"
      :visibleColorPicker="undefined"
      :nodeToTableItem="nodeToTableItem"
      :filterRange="filterRange"
      :dark="computedDark"
      @change="updateOpacityNodes"
      @select="updateSelectedNodes"
      @pick="() => {}"
    />
  </div>
</template>

<style>
.dark {
  color: white !important;
}
.help-circle {
  position: absolute;
  left: 0;
  top: 0;
  width: 30px;
}
.widget-container {
  display: flex;
  flex-direction: column;
  row-gap: 10px;
  position: relative;
  margin: 10px;
}
.indented {
  margin: 0px 20px;
  max-width: calc(100% - 40px);
}
.histogram-canvas {
  height: 100px;
}
.histogram-labels {
  display: flex;
  position: absolute;
  width: 100%;
  top: 35px;
  z-index: 3;
  justify-content: space-between;
  font-weight: 900;
  -webkit-text-fill-color: white;
  -webkit-text-stroke-width: 1px;
  -webkit-text-stroke-color: black;
}
.histogram-labels.shifted {
  top: 140px;
}
.gradient-box {
  height: 45px;
  width: 100%;
  position: absolute;
  top: -30px;
  z-index: -1;
}
.color-line {
  z-index: 2;
  outline: 1px solid black;
  position: relative;
  margin: 20px 0px;
}
.color-line.dark {
  outline: 1px solid white;
}
.update-btn {
  justify-self: flex-end;
}
.tall-gap {
  height: 100px;
}
</style>
