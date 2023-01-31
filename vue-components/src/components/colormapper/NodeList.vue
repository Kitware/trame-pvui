<script lang="ts">
import RangeEditor from './RangeEditor.vue';
export default {
  components: { RangeEditor },
  props: {
    nodes: {
      type: Array,
      required: true,
    },
    selectedNodes: {
      type: Array,
      required: true,
    },
    visibleColorPicker: {
      type: Number || undefined,
      default: undefined,
    },
    filterRange: {
      type: Array || undefined,
      default: undefined,
    },
    nodeToTableItem: {
      type: Function,
      required: true,
    },
    opacityMode: {
      type: Boolean,
      default: false,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      colorPickerWidth: 300,
      colorPickerValue: {
        r: 255,
        g: 0,
        b: 0,
      },
      fullRange: undefined,
      tableRange: undefined,
      filteredNodeList: [],
    };
  },
  methods: {
    getNodesRange() {
      const values = this.nodeList.map((node) => node.value);
      return [Math.min(...values), Math.max(...values)];
    },
    nodeIndexToColorPickerValue(node) {
      const rgb = node.slice(1).map((value) => value * 255);
      // TODO: change based on interpolation mode
      return {
        r: rgb[0],
        g: rgb[1],
        b: rgb[2],
      };
    },
    resetTableRange() {
      this.tableRange = [...this.fullRange];
    },
    toggleSelectNode(item, single = false) {
      this.$emit('pick', undefined);
      if (this.selectedNodes.map((node) => node.id).includes(item.id)) {
        const newSelectedNodes = this.selectedNodes.filter(
          (node) => node.id != item.id
        );
        this.$emit('select', newSelectedNodes);
      } else {
        if (single) this.$emit('select', [item]);
        else {
          const newSelectedNodes = [...this.selectedNodes];
          newSelectedNodes.push(item);
          this.$emit('select', newSelectedNodes);
        }
      }
    },
    toggleSelectAll() {
      if (this.selectedNodes.length == this.filteredNodeList.length) {
        this.$emit('select', []);
      } else {
        this.$emit('select', this.filteredNodeList);
      }
    },
    toggleColorPicker(item) {
      if (this.visibleColorPicker !== item.id) {
        this.$emit('pick', item.id);
      } else {
        this.$emit('pick', undefined);
      }
    },
    changeNodeValue(index, newValue) {
      if (!newValue) return;
      const newList = [...this.nodes];
      newList[index][0] = parseInt(newValue);
      this.$emit('change', newList);
    },
    removeSelectedNodes() {
      const newList = [...this.nodes];
      this.selectedNodes.forEach((node) => {
        newList.splice(node.id, 1);
      });
      this.$emit('change', newList);
      this.$emit('select', []);
    },
    addNode() {
      const newNode = [0, 0, 0, 0];
      const newList = [...this.nodes];
      newList.push(newNode);
      this.$emit('select', [
        this.nodeToTableItem(newNode, newList.length - 1, this.opacityMode),
      ]);
      this.$emit('change', newList);
    },
    updateColorOfSelectedNode(newValue) {
      this.colorPickerValue = newValue;
      const targetNode = this.nodeList.find(
        (node) => node.id == this.visibleColorPicker
      );
      const newList = [...this.nodes];
      const newRGB = Object.values(newValue).map(
        (ratio: number) => ratio / 255
      );
      newList[this.visibleColorPicker] = [targetNode.value, ...newRGB];
      this.$emit('change', newList);
    },
    updateList(newItems) {
      const newList = [...this.nodes];
      newItems.forEach((item) => {
        newList[item.id] = [item.value, ...item.rgb.map((v) => v / 255)];
      });
      this.$emit('change', newList);
    },
  },
  computed: {
    nodeList() {
      return this.nodes.map((node, index) =>
        this.nodeToTableItem(node, index, this.opacityMode)
      );
    },
    headers() {
      return [
        {
          text: 'swatch',
          value: 'rgb',
          sortable: false,
          width: '50px',
        },
        { text: 'value', value: 'value', align: 'start' },
      ];
    },
  },
  watch: {
    tableRange() {
      const shownRange = this.tableRange.map((v) => parseInt(v));
      this.filteredNodeList = this.nodeList.filter(
        (node) => node.value >= shownRange[0] && node.value <= shownRange[1]
      );
    },
    nodes() {
      const shownRange = this.tableRange.map((v) => parseInt(v));
      this.filteredNodeList = this.nodeList.filter(
        (node) => node.value >= shownRange[0] && node.value <= shownRange[1]
      );
      this.fullRange = this.getNodesRange();
      this.tableRange = [...this.fullRange];
    },
    visibleColorPicker() {
      if (this.visibleColorPicker !== undefined) {
        this.colorPickerValue = this.nodeIndexToColorPickerValue(
          this.nodes[this.visibleColorPicker]
        );
        this.$nextTick(() => {
          if (this.$refs.colorPicker) {
            this.colorPickerWidth = this.$refs.colorPicker.$el.clientWidth;
          }
        });
      }
    },
    filterRange() {
      this.tableRange = this.filterRange;
    },
  },
  mounted() {
    this.fullRange = this.getNodesRange();
    this.tableRange = [...this.fullRange];
  },
};
</script>

<template>
  <v-data-table
    :value="selectedNodes"
    ref="table"
    :items="filteredNodeList"
    :headers="headers"
    :dark="dark"
    sort-by="value"
    must-sort
    fixed-header
    hide-default-footer
    height="200px"
    class="mt-3"
    dense
    @select="(newSelection) => this.$emit('select', newSelection)"
  >
    <template #top>
      <div
        v-if="tableRange"
        class="px-3 d-flex caption"
        style="column-gap: 5px; align-items: center; flex-wrap: wrap"
      >
        Filter table by range
        <v-text-field
          :value="tableRange[0]"
          class="mt-0 pt-0 value-input"
          hide-details
          single-line
          type="number"
          :min="fullRange[0]"
          :max="tableRange[1]"
          @input="$set(tableRange, 0, $event)"
        ></v-text-field>
        ...
        <v-text-field
          :value="tableRange[1]"
          class="mt-0 pt-0 value-input"
          hide-details
          single-line
          type="number"
          style="width: 60px"
          :min="tableRange[0]"
          :max="fullRange[1]"
          @input="$set(tableRange, 1, $event)"
        ></v-text-field>
        <div style="flex-grow: 5">
          <v-icon @click="resetTableRange"> mdi-arrow-expand-vertical </v-icon>
        </div>
      </div>
      <div :dark="dark" class="px-3 d-flex" style="align-items: center">
        <div class="text-caption">
          {{ nodeList.length }} Control Points
          <i>
            ({{ filteredNodeList.length }} shown,
            {{ selectedNodes.length }} selected)
          </i>
        </div>
      </div>
    </template>
    <template #item="{ item }">
      <tr
        :class="
          (selectedNodes.map((node) => node.id).includes(item.id)
            ? 'selected'
            : '') + (dark ? ' dark' : '')
        "
        @click="() => toggleSelectNode(item)"
      >
        <td style="width: 50px">
          <div
            :id="'color-square-' + item.id"
            :class="dark ? `color-square dark` : `color-square`"
            :style="`background-color: ` + item.rgbString"
            @click="
              (e) => {
                e.stopPropagation();
                toggleColorPicker(item);
              }
            "
          ></div>
          <v-card
            ref="colorPicker"
            class="color-editor-pane"
            v-if="visibleColorPicker == item.id"
            :ripple="false"
            @click="(e) => e.stopPropagation()"
          >
            <v-icon
              style="float: right"
              @click="
                (e) => {
                  e.stopPropagation();
                  $emit('pick', undefined);
                }
              "
            >
              mdi-close
            </v-icon>
            <v-lazy>
              <v-color-picker
                :value="colorPickerValue"
                canvas-height="65px"
                :hide-canvas="colorPickerValue === undefined"
                :width="`${colorPickerWidth}`"
                @input="updateColorOfSelectedNode"
              />
            </v-lazy>
          </v-card>
        </td>
        <td>
          <v-text-field
            :value="item.value"
            class="value-input"
            hide-details
            single-line
            type="number"
            @click.stop
            @input="(newValue) => changeNodeValue(item.id, newValue)"
          />
        </td>
      </tr>
    </template>
    <template #footer>
      <div
        class="d-flex mt-2"
        style="justify-content: space-between; flex-wrap: wrap; row-gap: 5px"
      >
        <v-btn small @click="toggleSelectAll">
          {{
            selectedNodes.length != filteredNodeList.length
              ? 'Select'
              : 'Deselect'
          }}
          all
        </v-btn>
        <v-btn small :disabled="selectedNodes.length > 0" @click="addNode">
          + New
        </v-btn>
        <v-btn
          small
          :disabled="selectedNodes.length == 0"
          @click="removeSelectedNodes"
        >
          Delete
          {{ selectedNodes.length > 0 ? '(' + selectedNodes.length + ')' : '' }}
        </v-btn>
      </div>
      <range-editor
        v-if="fullRange && !opacityMode"
        :selectedNodes="selectedNodes"
        :dark="dark"
        :fullRange="fullRange"
        @change="updateList"
      />
    </template>
  </v-data-table>
</template>

<style>
tr.selected {
  background-color: rgba(0, 0, 0, 0.1);
}
tr.selected.dark {
  background-color: rgba(255, 255, 255, 0.2);
}
.value-input {
  width: 70px;
  min-width: 60px;
  max-width: 70px;
  padding: 0;
  margin: 0;
}
.color-square {
  height: 25px;
  width: 25px;
  border: 3px solid black;
  float: right;
}
.color-square.dark {
  border: 3px solid white;
}
.color-editor-pane {
  position: absolute;
  top: 35px;
  left: 70px;
  width: calc(100% - 75px);
  height: calc(100% - 40px);
  background-color: inherit;
  z-index: 2;
  padding: 5px;
  text-align: center;
}
.v-data-table__wrapper {
  position: relative;
}
.v-color-picker__preview {
  width: 100%;
  margin-right: 20px;
}
.v-color-picker__hue,
.v-color-picker__edit {
  margin: 3px !important;
}
.v-color-picker__controls {
  padding: 5px 10px;
}
.v-btn.v-btn--icon.v-btn--round.v-size--small,
.v-color-picker__dot {
  display: none;
}
</style>
