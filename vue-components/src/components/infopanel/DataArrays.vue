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
  <v-data-table dense :headers="headers" :items="items"> </v-data-table>
</template>
