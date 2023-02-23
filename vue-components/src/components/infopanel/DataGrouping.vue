<script>
import { defineComponent } from 'vue';

export default defineComponent({
  props: {
    dataGrouping: {
      type: Array,
      required: true,
    },
  },
  setup(props) {
    function fillChildren(node, childrenList) {
      if (!node) return node;
      return Object.assign(node, {
        children: childrenList
          .filter((c) => node.children.includes(c.id))
          .map((c) => fillChildren(c, childrenList)),
      });
    }

    const tree = [
      fillChildren(
        props.dataGrouping.find((e) => e.name == 'Root' && e.path === '/Root'),
        props.dataGrouping
      ),
    ];
    console.log(tree);
    return {
      tree,
    };
  },
});
</script>

<template>
  <v-treeview :items="tree" dense> </v-treeview>
</template>
