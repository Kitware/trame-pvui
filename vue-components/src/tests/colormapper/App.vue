<script lang="ts">
import components from '../../components';
const { Colormapper } = components;

export default {
  name: 'HomePage',
  components: {
    Colormapper,
  },
  data() {
    const histogramData = {
      counts: [
        7417676, 0, 14464981, 7114126, 5670523, 164754, 16188, 5310, 3273, 8321,
      ],
      range: [-2048.0, 3071.0],
    };
    const colors = [
      [-2200, 1, 0, 0],
      [-2048, 0, 1, 0],
      [511.5, 0, 0, 1],
      [3071, 0, 0, 0],
      [3300, 1, 1, 1],
    ];

    const opacities = [
      [-2048, 1, 0.5, 0],
      [511.5, 0.5, 0.5, 0],
      [3071, 1, 0.5, 0],
    ];

    return {
      histogramData,
      colors,
      opacities,
    };
  },
};
</script>

<template>
  <div id="app">
    <v-app>
      <div class="d-flex">
        <div class="container-1">
          <colormapper
            :histogram-data="histogramData"
            :colors="colors"
            :opacities="opacities"
            dark
          />
        </div>
        <div class="container-2">
          <colormapper
            :histogram-data="histogramData"
            :colors="colors"
            :opacities="opacities"
          />
        </div>
      </div>
    </v-app>
  </div>
</template>

<style scoped>
.container-1 {
  margin: 10px;
  padding: 10px;
  width: 400px;
  background-color: black;
}
.container-2 {
  margin: 10px;
  padding: 10px;
  border: 1px dashed black;
  width: 700px;
}
</style>
