<script>
import { defineComponent, ref } from 'vue';
import DataArrays from './DataArrays.vue';
import DataGrouping from './DataGrouping.vue';

export default defineComponent({
  methods: {
    format_integer(num) {
      return num.toLocaleString();
    },
    /* TODO make this configurable */
    format_float(num) {
      return num.toFixed(3);
    },
    format_memory(num_bytes) {
      const size_units = ['TB', 'GB', 'MB', 'kB', 'bytes'];
      const size = size_units.length;
      for (const [i, suffix] of size_units.entries()) {
        const exponent = size - 2 - i;
        const divisor = 1000 ** exponent;
        if (num_bytes > divisor) {
          return num_bytes / divisor + ' ' + suffix;
        }
      }
      return 'None';
    },
  },
  components: { DataGrouping, DataArrays },
  props: {
    selectedNode: {
      type: String,
      required: true,
    },
    fileProperties: {
      type: Object,
      required: true,
    },
    dataGrouping: {
      type: Array,
      required: true,
    },
    dataStatistics: {
      type: Object,
      required: true,
    },
    dataArrays: {
      type: Array,
      required: true,
    },
    timesteps: {
      type: Array,
      required: false,
    },
  },
  setup(_props, { emit }) {
    const expanded = ref([0]);

    function setSelectedNode(selectedNode) {
      emit('setSelectedNode', selectedNode);
    }

    return {
      expanded,
      setSelectedNode,
    };
  },
});
</script>

<template>
  <v-card elevation="3">
    <v-card-title class="dark-title">Information</v-card-title>
    <v-expansion-panels v-model="expanded" accordion multiple>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          File Properties
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-simple-table dense>
            <tbody>
              <tr>
                <td class="labelColumn">Name</td>
                <td class="valueColumn">
                  <div v-if="fileProperties['name'] != ''">
                    {{ fileProperties['name'] }}
                  </div>
                  <div v-else>N/A</div>
                </td>
              </tr>

              <tr>
                <td class="labelColumn">Path</td>
                <td class="valueColumn">
                  <div v-if="fileProperties['name'] != ''">
                    {{ fileProperties['path'] }}
                  </div>
                  <div v-else>N/A</div>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Grouping
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <data-grouping
            :dataGrouping="dataGrouping"
            @select="setSelectedNode"
          />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Statistics
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-simple-table dense>
            <tbody>
              <tr>
                <td class="labelColumn">Type</td>
                <td class="valueColumn">{{ dataStatistics['type'] }}</td>
              </tr>
              <tr>
                <td class="labelColumn"># of Cells</td>
                <td class="valueColumn">
                  {{ format_integer(dataStatistics['num_cells']) }}
                </td>
              </tr>
              <tr>
                <td class="labelColumn"># of Points</td>
                <td class="valueColumn">
                  {{ format_integer(dataStatistics['num_points']) }}
                </td>
              </tr>
              <tr>
                <td class="labelColumn"># of Timesteps</td>
                <td class="valueColumn">
                  {{ format_integer(dataStatistics['num_timesteps']) }}
                </td>
              </tr>
              <tr>
                <td class="labelColumn">Current Time</td>
                <td class="valueColumn">
                  {{ format_float(dataStatistics['current_time']) }} (range: [{{
                    format_float(dataStatistics['time_range'][0])
                  }}, {{ format_float(dataStatistics['time_range'][1]) }} ] )
                </td>
              </tr>
              <tr>
                <td class="labelColumn">Memory</td>
                <td class="valueColumn">
                  {{ format_memory(dataStatistics['memory']) }}
                </td>
              </tr>
              <tr>
                <td class="labelColumn">Bounds</td>
                <td class="valueColumn">
                  <span v-for="index in 3" :key="index">
                    {{ format_float(dataStatistics['bounds'][index]) }} to
                    {{ format_float(dataStatistics['bounds'][index + 1]) }}
                    <span class="detail">
                      (delta:
                      {{
                        format_float(
                          dataStatistics['bounds'][index + 1] -
                            dataStatistics['bounds'][index]
                        )
                      }})
                    </span>
                    <span v-if="index != 3"> <br /> </span>
                  </span>
                </td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Arrays
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <data-arrays :dataArrays="dataArrays" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel v-if="timesteps">
        <v-expansion-panel-header class="font-weight-bold">
          Timesteps
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-simple-table dense>
            <thead>
              <tr>
                <th class="time-header">Index</th>
                <th class="time-header">Time</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="(value, index) in timesteps" :key="index">
                <td class="labelColumn">{{ index }}</td>
                <td class="valueColumn">{{ value }}</td>
              </tr>
            </tbody>
          </v-simple-table>
        </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<style scoped>
.dark-title {
  background-color: #444;
  color: white;
}
.v-card {
  overflow: auto;
}

/* Formatting options for the first column i.e. the one containing the label */
.labelColumn {
  color: #444;
  vertical-align: top;
  /* Fixed column size to longest label without breaking */
  width: 1%;
  white-space: nowrap;
}
/* Formatting options for the second column i.e. the one containing the value */
.valueColumn {
  color: #777;
  /* Fixed column size to longest label without breaking */
  width: 1%;
  white-space: nowrap;
}

.detail {
  font-size: 95%;
}

.time-header {
  color: #424242ff;
  background-color: #ecececff;
}
</style>
