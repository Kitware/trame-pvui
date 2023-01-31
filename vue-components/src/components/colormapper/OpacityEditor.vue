<script lang="ts">
import clamp from '../../utils/clamp';
import { makeDraggableSVG } from '../../utils/drag';
import { Chart, registerables } from 'chart.js';
import 'chartjs-plugin-dragdata';
Chart.register(...registerables);

const chartMargins = {
  x: 30,
  y: 10,
};

function registerPlugin() {
  Chart.register({
    id: 'advanced_line_controls',
    beforeDatasetsDraw: (chart) => {
      const that = chart.config.options.plugins['advanced_line_controls'];
      const { ctx } = chart;
      const { w, h } = that.dims;

      ctx.lineWidth = 3;
      ctx.lineCap = 'round';
      ctx.fillStyle = that.gradient;
      if (that.dark) ctx.strokeStyle = '#fff';
      for (var i = 0; i < that.currentData.length - 1; i++) {
        let pointA = that.toContextCoords(that.currentData[i]);
        let pointB = that.toContextCoords(that.currentData[i + 1]);
        const midpoint = {
          x: pointA.x + (pointB.x - pointA.x) * pointA.m,
          y: pointA.y + (pointB.y - pointA.y) * 0.5,
        };

        if (i === 0) {
          ctx.beginPath();
          ctx.moveTo(pointA.x, pointA.y);
        }
        ctx.bezierCurveTo(
          pointA.x + (midpoint.x - pointA.x) * pointA.s,
          pointA.y,
          midpoint.x,
          midpoint.y - (midpoint.y - pointA.y) * pointA.s,
          midpoint.x,
          midpoint.y
        );
        ctx.bezierCurveTo(
          midpoint.x,
          midpoint.y + (pointB.y - midpoint.y) * pointA.s,
          pointB.x - (pointB.x - midpoint.x) * pointA.s,
          pointB.y,
          pointB.x,
          pointB.y
        );
      }
      ctx.stroke();
      ctx.lineWidth = 0;
      ctx.lineTo(w + chartMargins.x, h + chartMargins.y);
      ctx.lineTo(chartMargins.x, h + chartMargins.y);
      ctx.closePath();
      ctx.fill();

      return false; // cancel datasets draw
    },
  });
}

export default {
  props: {
    dark: {
      type: Boolean,
      default: false,
    },
    dataRange: {
      type: Array,
      required: true,
    },
    opacityNodes: {
      type: Array,
      required: true,
    },
    selectedNodes: {
      type: Array,
      required: true,
    },
  },
  data() {
    return {
      currentData: [],
      focusedPoint: undefined,
    };
  },
  computed: {
    chartOptions() {
      return {
        type: 'line',
        data: {
          datasets: [
            {
              label: 'Opacity',
              data: this.currentData.map((point) => ({
                x: point.x,
                y: point.y,
              })),
              pointHitRadius: 15,
              borderColor: this.dark ? '#fff' : '#000',
            },
          ],
        },
        options: {
          responsive: true,
          animation: false,
          maintainAspectRatio: false,
          scales: {
            y: { min: 0, max: 1 },
            x: { min: 0, max: 100, display: false, type: 'linear' },
          },
          layout: { padding: { right: 30 } },
          onHover: function (e) {
            const point = e.chart.getElementsAtEventForMode(
              e,
              'nearest',
              { intersect: true },
              false
            );
            if (point.length) e.native.target.style.cursor = 'grab';
            else e.native.target.style.cursor = 'default';
          },
          onClick: this.clickChart,
          plugins: {
            advanced_line_controls: this,
            tooltip: {
              callbacks: {
                title: function (context) {
                  return this.toTrueValue(context[0].parsed.x);
                }.bind(this),
              },
            },
            legend: { display: false },
            dragData: {
              round: 1,
              dragX: true,
              showTooltip: true,
              onDrag: (e, dIndex, index) => {
                e.target.style.cursor = 'grabbing';
                const point = this.opacityNodes[index];
                this.$emit('select', [
                  {
                    id: index,
                    index,
                    rgb: [0, 0, 0, point[1]],
                    rgbString: `rgb(0, 0, 0, ${point[1]})`,
                  },
                ]);
                this.update();
              },
              onDragEnd: (e) => {
                e.target.style.cursor = 'default';
              },
            },
          },
        },
      };
    },
    dims() {
      const chart = this.$refs.chartJSContainer;
      const { width, height } = chart;
      const w = width - chartMargins.x * 2;
      const h = height - chartMargins.y * 2;
      return { w, h };
    },
  },
  methods: {
    toContextCoords(point) {
      if (!point) return undefined;
      const { w, h } = this.dims;
      return {
        x: (point.x / 100) * w + chartMargins.x,
        y: h - point.y * h + chartMargins.y,
        m: point.m,
        s: point.s,
      };
    },
    toRealData(location) {
      if (!location) return undefined;
      const { w, h } = this.dims;
      return {
        x: ((location.x - chartMargins.x) / w) * 100,
        y: ((location.y - chartMargins.y - h) * -1) / h,
      };
    },
    toTrueValue(x) {
      return Math.round(
        (x / 100) * (this.dataRange[1] - this.dataRange[0]) + this.dataRange[0]
      );
    },
    toProportionalValue(x) {
      return (
        ((x - this.dataRange[0]) / (this.dataRange[1] - this.dataRange[0])) *
        100
      );
    },
    insertSortedByFunction(array, value, func) {
      // from https://stackoverflow.com/a/21822316
      var low = 0;
      var high = array.length;

      while (low < high) {
        var mid = (low + high) >>> 1;
        if (func(array[mid], value)) low = mid + 1;
        else high = mid;
      }
      array.splice(low, 0, value);
      return array;
    },
    addDatum(x, y, m, s) {
      this.chartInstance.data.labels = this.insertSortedByFunction(
        this.chartInstance.data.labels,
        x,
        (a, b) => a < b
      );
      this.currentData = this.insertSortedByFunction(
        this.currentData,
        { x, y, m, s },
        (a, b) => a.x < b.x
      );
    },
    clickChart(e) {
      const { height, width } = e.chart.chartArea;
      const x = clamp(Math.round(((e.x - 40) / width) * 100), 0, 100);
      const y = clamp(
        parseFloat(((height - (e.y - 10)) / height).toFixed(1)),
        0,
        1
      );
      this.addDatum(x, y, 0.5, 0);
      this.update();
    },
    focusSelected() {
      if (this.selectedNodes.length > 0) {
        this.focusedPoint = this.selectedNodes[0].index;
      }
      this.chartInstance.update();
    },
    drawDraggables() {
      const svgns = 'http://www.w3.org/2000/svg';
      const editableNodesContainer = this.$refs.editableNodesContainer;
      if (!editableNodesContainer) return undefined;

      editableNodesContainer.innerHTML = '';
      let primaryFill = '#000';
      let secondaryFill = '#fff';
      if (this.dark) {
        primaryFill = '#fff';
        secondaryFill = '#000';
      }

      this.currentData.map(this.toContextCoords).forEach((point) => {
        this.drawDraggableNode(
          point.x,
          point.y,
          svgns,
          editableNodesContainer,
          primaryFill
        );
      });
      if (
        this.focusedPoint &&
        this.focusedPoint < this.currentData.length - 1
      ) {
        const pointA = this.currentData[this.focusedPoint];
        const pointB = this.currentData[this.focusedPoint + 1];
        const pointC = this.currentData[this.focusedPoint - 1];
        const focusedControlPoints = [
          { x: pointA.x, y: (pointB.y - pointA.y) * pointA.s + pointA.y },
          { x: (pointB.x - pointA.x) * pointA.m + pointA.x, y: pointA.y },
          { x: pointC.x + (pointA.x - pointC.x) * pointC.m, y: pointA.y },
        ];
        focusedControlPoints
          .map(this.toContextCoords)
          .forEach((cp: { x: number; y: number }, index) => {
            if (cp) {
              this.drawDraggableControlPoint(
                cp.x,
                cp.y,
                index,
                svgns,
                editableNodesContainer,
                primaryFill,
                secondaryFill
              );
            }
          });
      }
    },
    drawDraggableNode(x, y, svgns, container, fill) {
      var circle = document.createElementNS(svgns, 'circle');
      circle.setAttributeNS(null, 'cx', x);
      circle.setAttributeNS(null, 'cy', y);
      circle.setAttributeNS(null, 'r', '3');
      circle.setAttributeNS(null, 'fill', fill);
      container.appendChild(circle);
    },
    drawDraggableControlPoint(
      x,
      y,
      index,
      svgns,
      container,
      primaryFill,
      secondaryFill
    ) {
      var control = document.createElementNS(svgns, 'circle');
      var shifted = { x, y: y - 5 };
      if (index === 1) shifted = { x: x + 10, y };
      if (index === 2) shifted = { x: x - 10, y };
      control.setAttributeNS(null, 'cx', `${shifted.x}`);
      control.setAttributeNS(null, 'cy', `${shifted.y}`);
      control.setAttributeNS(null, 'r', '5');
      control.setAttributeNS(null, 'stroke', primaryFill);
      control.setAttributeNS(null, 'fill', secondaryFill);
      control.setAttributeNS(null, 'class', 'draggable');
      control.setAttributeNS(null, 'id', index);
      control.setAttributeNS(null, 'pointer-events', 'all');
      container.appendChild(control);
    },
    validateControlPointDrag(selected, newLocation) {
      if (
        this.focusedPoint &&
        this.focusedPoint < this.currentData.length - 1
      ) {
        let moveX = true;
        let moveY = true;
        const newReal = this.toRealData(newLocation);
        if (newReal.y > 1 || newReal.y < 0) moveY = false;
        let pointA = this.currentData[this.focusedPoint];
        let pointB = this.currentData[this.focusedPoint + 1];
        let pointC = this.currentData[this.focusedPoint - 1];
        if (selected.id === '1') {
          moveY = false;
          if (newReal.x < pointA.x || newReal.x > pointB.x) moveX = false;
        } else if (selected.id === '2') {
          moveY = false;
          if (newReal.x < pointC.x || newReal.x > pointA.x) moveX = false;
        } else if (selected.id === '0') {
          moveX = false;
          if (pointA.y < pointB.y) {
            if (newReal.y < pointA.y || newReal.y > pointB.y) moveY = false;
          } else {
            if (newReal.y < pointB.y || newReal.y > pointA.y) moveY = false;
          }
        }
        return [moveX, moveY];
      }
      return [false, false];
    },
    dragControlPoint(selected, newLocation) {
      newLocation = this.toRealData(newLocation);
      if (this.focusedPoint < this.currentData.length - 1) {
        const pointA = this.currentData[this.focusedPoint];
        const pointB = this.currentData[this.focusedPoint + 1];
        const pointC = this.currentData[this.focusedPoint - 1];
        if (selected.id === '0') {
          // vertical cp; controls sharpness
          const percentage = (newLocation.y - pointA.y) / (pointB.y - pointA.y);
          this.currentData[this.focusedPoint].s = percentage;
          // control left-side sharpness if left side exists
          if (this.focusedPoint > 0) {
            this.currentData[this.focusedPoint - 1].s = percentage;
          }
        } else if (selected.id === '1') {
          // horizontal cp; controls midpoint
          const percentage = (newLocation.x - pointA.x) / (pointB.x - pointA.x);
          this.currentData[this.focusedPoint].m = percentage;
        } else if (selected.id === '2') {
          // horizontal cp; controls previous midpoint
          const percentage = (newLocation.x - pointC.x) / (pointA.x - pointC.x);
          this.currentData[this.focusedPoint - 1].m = percentage;
        }
      }
      this.chartInstance.update();
      this.update();
    },
    populate() {
      this.currentData = [];
      this.opacityNodes.forEach(([x, y, m, s]) => {
        this.addDatum(this.toProportionalValue(x), y, m, s);
      });
      this.chartInstance.data.datasets[0].data = this.currentData;
      this.chartInstance.update();
      this.drawDraggables();
    },
    update() {
      const newList = this.currentData.map(({ x, y, m, s }) => {
        return [this.toTrueValue(x), y, m, s];
      });
      this.$emit('update', newList);
    },
  },
  created() {
    registerPlugin();
  },
  mounted() {
    this.canvas = document.getElementById(
      'chartJSContainer'
    ) as HTMLCanvasElement;
    this.ctx = this.canvas.getContext('2d');
    this.chartInstance = new Chart(this.ctx, this.chartOptions);

    // create gradient fill
    this.gradient = this.ctx.createLinearGradient(0, 0, 0, 100);
    this.gradient.addColorStop(1, 'transparent');
    this.gradient.addColorStop(0, this.dark ? 'white' : 'black');

    makeDraggableSVG(
      this.$refs.editableNodesContainer,
      this.validateControlPointDrag,
      this.dragControlPoint
    );
    this.focusSelected();
    this.populate();
  },
  watch: {
    opacityNodes: {
      handler() {
        this.populate();
      },
      deep: true,
    },
    selectedNodes: {
      handler() {
        this.focusSelected();
      },
      deep: true,
    },
    dark: registerPlugin,
  },
};
</script>

<template>
  <div class="curve-editor">
    <div class="responsive-size">
      <canvas id="chartJSContainer" ref="chartJSContainer" height="50"></canvas>
      <svg
        ref="editableNodesContainer"
        class="nodes-container"
        xmlns="http://www.w3.org/2000/svg"
        width="100%"
      />
    </div>
    <div class="x-labels">
      <p>{{ dataRange[0] }}</p>
      <p>{{ dataRange[1] }}</p>
    </div>
  </div>
</template>

<style scoped>
.curve-editor {
  height: 110px;
  width: calc(100% + 20px);
  position: absolute;
  top: 23px;
  left: -10px;
  z-index: 5;
}
.responsive-size {
  position: relative;
  height: 100%;
  width: 100%;
}
.nodes-container {
  position: absolute;
  top: 0;
  pointer-events: none;
}
.x-labels {
  display: flex;
  justify-content: space-between;
  padding: 0px 30px;
  margin-top: -10px;
  width: 100%;
}
</style>
