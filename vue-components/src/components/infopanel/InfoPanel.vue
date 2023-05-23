<script>
import { defineComponent, ref } from 'vue';
import DataArrays from './DataArrays.vue';
import DataGrouping from './DataGrouping.vue';

export default defineComponent({
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
    byteFormatter: {
      type: Function,
      required: false,
      default: (bytes) => bytes + ' bytes',
    },
    integerFormatter: {
      type: Function,
      required: false,
      default: (num) => num,
    },
    floatFormatter: {
      type: Function,
      required: false,
      default: (num) => num,
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
          <div v-if="fileProperties">
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
          </div>
          <div v-else>N/A</div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Grouping
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-if="dataGrouping">
            <data-grouping
              :dataGrouping="dataGrouping"
              @select="setSelectedNode"
            />
          </div>
          <div v-else>N/A</div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Statistics
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-if="dataStatistics">
            <v-simple-table dense>
              <tbody>
                <tr>
                  <td class="labelColumn">Type</td>
                  <td class="valueColumn">{{ dataStatistics['type'] }}</td>
                </tr>
                <tr>
                  <td class="labelColumn"># of Cells</td>
                  <td class="valueColumn">
                    {{ integerFormatter(dataStatistics['num_cells']) }}
                  </td>
                </tr>
                <tr>
                  <td class="labelColumn"># of Points</td>
                  <td class="valueColumn">
                    {{ integerFormatter(dataStatistics['num_points']) }}
                  </td>
                </tr>
                <tr v-if="dataStatistics['num_timesteps'] != 0">
                  <td class="labelColumn"># of Timesteps</td>
                  <td class="valueColumn">
                    {{ integerFormatter(dataStatistics['num_timesteps']) }}
                  </td>
                </tr>
                <tr v-if="dataStatistics['num_timesteps'] != 0">
                  <td class="labelColumn">Current Time</td>
                  <td class="valueColumn">
                    {{ floatFormatter(dataStatistics['current_time']) }} (range:
                    [{{ floatFormatter(dataStatistics['time_range'][0]) }},
                    {{ floatFormatter(dataStatistics['time_range'][1]) }} ] )
                  </td>
                </tr>
                <tr>
                  <td class="labelColumn">Memory</td>
                  <td class="valueColumn">
                    {{ byteFormatter(dataStatistics['memory']) }}
                  </td>
                </tr>
                <tr>
                  <td class="labelColumn">Bounds</td>
                  <td class="valueColumn">
                    <span v-for="index in 3" :key="index">
                      {{ floatFormatter(dataStatistics['bounds'][index]) }} to
                      {{ floatFormatter(dataStatistics['bounds'][index + 1]) }}
                      <span class="detail">
                        (delta:
                        {{
                          floatFormatter(
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
          </div>
          <div v-else>N/A</div>
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Arrays
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <div v-if="dataArrays">
            <data-arrays :dataArrays="dataArrays" />
          </div>
          <div v-else>N/A</div>
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
