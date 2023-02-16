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
      dataXMLString:
        '<xml version="1.0">\
        <IOSS type="vtkDataAssembly" version="1.0" id="1">\
          <element_blocks id="0">\
            <block_1 id="1" label="block_1">\
              <dataset id="1"/>\
            </block_1>\
            <block_2 id="2" label="block_2">\
              <dataset id="2"/>\
            </block_2>\
          </element_blocks>\
          <node_sets id="1">\
            <node_list_1 id="1"/>\
            <node_list_100 id="100"/>\
          </node_sets>\
          <side_sets id="2">\
            <surface_4 id="4"/>\
          </side_sets>\
        </IOSS>\
      </xml>',
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
          name: 'DistanceToCenter',
          type: 'float',
          range: [0, 8.66],
        },
        {
          name: 'Polynomial',
          type: 'float',
          range: [1, 31.045],
        },
      ],
    };
  },
});
</script>

<template>
  <div id="app">
    <v-app>
      <info-panel
        :fileProperties="fileProperties"
        :dataXMLString="dataXMLString"
        :dataStatistics="dataStatistics"
        :dataArrays="dataArrays"
      />
    </v-app>
  </div>
</template>
