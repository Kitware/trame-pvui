<script>
import { defineComponent, ref } from 'vue';
import DataArrays from './DataArrays.vue';
import DataGrouping from './DataGrouping.vue';

export default defineComponent({
  components: { DataGrouping, DataArrays },
  props: {
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
  setup() {
    const expanded = ref([0]);

    return {
      expanded,
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
              <tr
                v-for="[key, value] in Object.entries(fileProperties)"
                :key="key"
              >
                <td>
                  {{
                    key.charAt(0).toUpperCase() +
                    key.substr(1).replace('_', ' ')
                  }}
                </td>
                <td>{{ value }}</td>
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
          <data-grouping :dataGrouping="dataGrouping" />
        </v-expansion-panel-content>
      </v-expansion-panel>
      <v-expansion-panel>
        <v-expansion-panel-header class="font-weight-bold">
          Data Statistics
        </v-expansion-panel-header>
        <v-expansion-panel-content>
          <v-simple-table dense>
            <tbody>
              <tr
                v-for="[key, value] in Object.entries(dataStatistics)"
                :key="key"
              >
                <td>
                  {{
                    key.charAt(0).toUpperCase() +
                    key.substr(1).replace('_', ' ')
                  }}
                </td>
                <td>{{ value }}</td>
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
            <tbody>
              <tr v-for="(value, index) in timesteps" :key="index">
                <td>{{ index }}</td>
                <td>{{ value }}</td>
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
</style>
