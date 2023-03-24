<script>
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    dataArrays: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    const headers = [
      {
        text: 'Name',
        value: 'name',
      },
      {
        text: 'Type',
        value: 'type',
        width: 100,
      },
      {
        text: 'Ranges',
        value: 'ranges',
        sortable: false,
      },
    ];
    const items = props.dataArrays;
    return {
      headers,
      items,
    };
  },
});
</script>

<template>
  <v-data-table dense :headers="headers" :items="items" item-key="name">
    <template v-slot:item="{ item }">
      <tr>
        <td class="nameColumn">{{ item.name }}</td>
        <td class="typeColumn">{{ item.type }}</td>
        <td class="rangeColumn">{{ item.ranges }}</td>
      </tr>
    </template>
  </v-data-table>
</template>

<style scoped>
::v-deep .v-data-table-header {
  color: #424242ff;
  background-color: #ecececff;
}

.nameColumn {
  color: #1565c0ff;
  background-color: #fbfbfbff;
}

.typeColumn {
  color: #1565c0ff;
  background-color: #fbfbfbff;
}

.rangeColumn {
  color: #1565c0ff;
  background-color: #fbfbfbff;
  /* Fixed column size to longest label without breaking */
  width: 1%;
  white-space: nowrap;
}
</style>
