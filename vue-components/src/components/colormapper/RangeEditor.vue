<script lang="ts">
export default {
  props: {
    selectedNodes: {
      type: Array,
      required: true,
    },
    fullRange: {
      type: Array,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  data() {
    return {
      originalRange: undefined,
      newRange: undefined,
    };
  },
  methods: {
    updateOriginalRange() {
      const values = this.selectedNodes.map((node) => node.value);
      this.originalRange = [Math.min(...values), Math.max(...values)];
      this.newRange = [...this.originalRange];
      this.newRange = this.newRange.map((v) => parseInt(v));
    },
    adjustRange() {
      this.newRange = this.newRange.map((v) => parseInt(v));
      const newNodesList = this.selectedNodes.map((node) => {
        const proportionalDistance =
          (node.value - this.originalRange[0]) /
          (this.originalRange[1] - this.originalRange[0]);
        const newValue =
          proportionalDistance * (this.newRange[1] - this.newRange[0]) +
          this.newRange[0];
        return Object.assign(node, { value: newValue });
      });
      this.$emit('change', newNodesList);
      this.updateOriginalRange();
    },
  },
  mounted() {
    this.updateOriginalRange();
  },
  watch: {
    selectedNodes() {
      this.updateOriginalRange();
    },
  },
};
</script>

<template>
  <v-card :dark="dark" v-if="selectedNodes.length > 1" class="mt-3 pa-3">
    Adjust range for selected nodes

    <div class="d-flex text-right" style="flex-direction: column">
      <div class="d-flex mb-2">
        <v-text-field
          :value="newRange[0]"
          class="mt-0 pt-0 value-input"
          hide-details
          single-line
          type="number"
          style="width: 70px"
          @input="$set(newRange, 0, $event)"
        ></v-text-field>
        <span class="mx-2">...</span>
        <v-text-field
          :value="newRange[1]"
          class="mt-0 pt-0 value-input"
          hide-details
          single-line
          type="number"
          style="width: 70px"
          @input="$set(newRange, 1, $event)"
        ></v-text-field>
      </div>
      <v-btn
        small
        v-if="
          newRange[0] != originalRange[0] || newRange[1] != originalRange[1]
        "
        @click="adjustRange"
        >Adjust</v-btn
      >
    </div>
  </v-card>
</template>
