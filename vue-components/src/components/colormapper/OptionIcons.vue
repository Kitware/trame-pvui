<script lang="ts">
export default {
  props: {
    options: {
      type: Object,
      required: true,
    },
    dark: {
      type: Boolean,
      default: false,
    },
  },
  methods: {
    getClassName(optionName) {
      let name = '';
      if (this.dark) name += 'inverted ';
      if (this.options[optionName]) name += 'enabled ';
      return name;
    },
    toggleOption(optionName) {
      this.$emit('update', optionName, !this.options[optionName]);
    },
  },
};
</script>

<template>
  <div class="icons-row">
    <img
      src="./opacity.png"
      height="25"
      width="25"
      :class="getClassName('opacityMode')"
      @click="toggleOption('opacityMode')"
    />
    <img
      src="./histogram.png"
      height="25"
      width="25"
      :class="getClassName('showHistogram')"
      @click="toggleOption('showHistogram')"
    />
  </div>
</template>

<style>
.icons-row {
  position: absolute;
  top: 0;
  left: 50px;
  right: 50px;
}
img {
  border-radius: 5px;
  padding: 1px;
  margin: 0px 2px;
}
img.inverted {
  filter: invert(100%);
}
img.enabled {
  background-color: rgba(1, 1, 1, 0.3);
}
</style>
