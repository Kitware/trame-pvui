<script>
import { computed, defineComponent, ref } from 'vue';

export default defineComponent({
  props: {
    dataGrouping: {
      type: Array,
      required: true,
    },
  },
  setup(props, { emit }) {
    const activeNode = ref();

    function updateActive(actives) {
      activeNode.value = actives[0];
      emit('select', activeNode.value);
    }

    function fillChildren(node, childrenList) {
      if (!node) return node;
      return Object.assign(node, {
        children: childrenList
          .filter((c) => node.children.includes(c.id))
          .map((c) => fillChildren(c, childrenList)),
      });
    }

    const tree = computed(() => [
      fillChildren(
        props.dataGrouping.find((e) => e.name == 'Root' && e.path === '/Root'),
        props.dataGrouping
      ),
    ]);

    return {
      activeNode,
      updateActive,
      tree,
    };
  },
});
</script>

<template>
  <v-treeview
    :items="tree"
    :active="[activeNode]"
    @update:active="updateActive"
    item-key="path"
    hoverable
    dense
    activatable
  >
  </v-treeview>
</template>
