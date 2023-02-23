<script lang="ts">
import { defineComponent } from 'vue';
import components from '../../components';

const { InfoPanel } = components;

export default defineComponent({
  name: 'HomePage',
  components: { InfoPanel },
  setup() {
    return {
      fileProperties: {
        name: 'Inspire.png',
        path: '/home/localUser/Documents/pv_examples/',
      },
      dataGrouping: [
        { id: 0, name: 'Root', path: '/Root', children: [1, 2, 3, 4, 5] },
        { id: 1, name: 'block_1', path: '/Root/block_1', children: [] },
        { id: 2, name: 'block_2', path: '/Root/block_2', children: [] },
        { id: 3, name: 'nodelist_1', path: '/Root/nodelist_1', children: [] },
        {
          id: 4,
          name: 'nodelist_100',
          path: '/Root/nodelist_100',
          children: [],
        },
        { id: 5, name: 'surface_4', path: '/Root/surface_4', children: [] },
      ],
      dataStatistics: {
        num_datasets: 2,
        type: 'Partitioned Dataset Collection',
        cells_count: 7152,
        points_count: 10088,
        time_steps: 44,
        current_time: 0.0042999,
        time_range: [0, 0.0042999],
        memory: '1.42578 MB',
        bounds: [
          [-121696, 9.08845],
          [-360042, 8.43386],
          [-19.3181, 11.6924],
        ],
      },
      dataArrays: [
        {
          name: 'ACCL',
          type: 'double',
          ranges: [
            [-4.965284006175352e-7, 3.212448973499704e-7],
            [-5.920087460253853e-7, 5.920081207477779e-7],
            [-0.000013328498425835278, 0.000010021663911174983],
          ],
          partial: false,
        },
        {
          name: 'DISPL',
          type: 'double',
          ranges: [
            [0, 0],
            [0, 0],
            [0, 0],
          ],
          partial: false,
        },
        {
          name: 'ids',
          type: 'idtype',
          ranges: [[1, 10088]],
          partial: false,
        },
        {
          name: 'VEL',
          type: 'double',
          ranges: [
            [0, 0],
            [0, 0],
            [-5000, 0],
          ],
          partial: false,
        },
        {
          name: 'EQPS',
          type: 'double',
          ranges: [[0, 0]],
          partial: false,
        },
        {
          name: 'ids',
          type: 'idtype',
          ranges: [[1, 7152]],
          partial: false,
        },
        {
          name: 'object_id',
          type: 'idtype',
          ranges: [[1, 2]],
          partial: false,
        },
        {
          name: 'Information Records',
          type: 'string',
          ranges: [
            '01/ Gen3D: can_half.g2d',
            '01/ can_half.g3d',
            '02/ Gen3D: block_half.g2d',
            '02/ block_half.g3d',
          ],
          partial: false,
        },
        {
          name: 'KE',
          type: 'double',
          ranges: [[2959999.75, 2959999.75]],
          partial: false,
        },
        {
          name: 'NSTEPS',
          type: 'double',
          ranges: [[0, 0]],
          partial: false,
        },
        {
          name: 'QA RCORDS',
          type: 'string',
          ranges: ['FASTQ 2.305/16/9414:09:31Gen3D   1.7'],
          partial: false,
        },
        {
          name: 'TMSTEP',
          type: 'double',
          ranges: [[2.4712693402761943e-7, 2.4712693402761943e-7]],
          partial: false,
        },
        {
          name: 'XMOM',
          type: 'double',
          ranges: [[0, 0]],
          partial: false,
        },
        {
          name: 'YMOM',
          type: 'double',
          ranges: [[0, 0]],
          partial: false,
        },
        {
          name: 'ZMOM',
          type: 'double',
          ranges: [[-1183.9998779296875, -1183.9998779296875]],
          partial: false,
        },
      ],
    };
  },
});
</script>

<template>
  <div id="app">
    <v-app>
      <div class="container">
        <info-panel
          :fileProperties="fileProperties"
          :dataGrouping="dataGrouping"
          :dataStatistics="dataStatistics"
          :dataArrays="dataArrays"
        />
      </div>
    </v-app>
  </div>
</template>

<style scoped>
.container {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 400px;
  height: min(600px, 100%);
  padding: 0;
  display: flex;
  justify-content: flex-end;
  flex-direction: column;
}
</style>
