<script>
import { defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    fileProperties: {
      type: Object,
      required: true,
    },
    dataXMLString: {
      type: String,
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
  <v-card class="container" elevation="3">
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
        <v-expansion-panel-content> TODO </v-expansion-panel-content>
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
        <v-expansion-panel-content> TODO </v-expansion-panel-content>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-card>
</template>

<style scoped>
.container {
  position: absolute;
  left: 0;
  bottom: 0;
  width: 400px;
  height: min(600px, 100%);
  padding: 0;
}
.dark-title {
  background-color: #444;
  color: white;
}
</style>
