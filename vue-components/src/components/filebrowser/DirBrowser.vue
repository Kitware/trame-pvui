<script lang="ts">
export default {
  props: {
    locationType: {
      type: String,
      required: true,
    },
    small: {
      type: Boolean,
      default: true,
    },
    allDirectories: {
      type: Array,
      required: true,
    },
    currentDir: {
      type: String,
      default: undefined,
    },
    dirContents: {
      type: Array,
      required: true,
    },
  },
  methods: {
    getIcon(type: string) {
      switch (type) {
        case 'folder':
          return 'mdi-folder';
        default:
          return 'mdi-file';
      }
    },
    selectItem(selected) {
      if (
        this.selectedItems.length === 0 &&
        selected.value &&
        !['folder', 'group'].includes(selected.item.type)
      ) {
        this.$emit('setFileName', selected.item.name);
      } else {
        this.$emit('setFileName', undefined);
      }
      if (selected.item.type === 'group') {
        if (selected.value) {
          this.selectedItems = [...this.selectedItems, ...selected.item.files];
        } else {
          this.selectedItems = this.selectedItems.filter(
            (i) => !selected.item.files.includes(i)
          );
        }
      }
      if (selected.value) {
        this.selectedItems.push(selected.item);
      } else {
        this.selectedItems = this.selectedItems.filter(
          (i) => i !== selected.item
        );
      }
      this.dirContents.forEach((item) => {
        if (item.type === 'group') {
          if (item.files?.every((i) => this.selectedItems.includes(i))) {
            this.selectedItems = [...this.selectedItems, item];
          } else {
            this.selectedItems = this.selectedItems.filter(
              (i) => i.name !== item.name
            );
          }
        }
      });
      this.selectedItems = this.selectedItems.filter((value, index, self) => {
        // no duplicates
        return self.indexOf(value) === index;
      });
      this.$emit('setCurrentSelected', this.selectedItems);
    },
    openItem(e, { item }) {
      if (item?.type === 'folder') {
        const folderLocation = this.currentDir + '/' + item.name;
        if (this.allDirectories.includes(folderLocation)) {
          this.$emit('setCurrentDir', {
            locationType: this.locationType,
            dirName: folderLocation,
          });
        } else {
          console.error(folderLocation, 'not found');
        }
      }
    },
    expandGroup(group) {
      if (this.expandedGroup === group.name) {
        this.expandedGroup = undefined;
      } else {
        this.expandedGroup = group.name;
      }
    },
    goBack() {
      console.log('Go back');
    },
    goForward() {
      console.log('Go forward');
    },
    goToParent() {
      const parent = this.currentDir.split('/').slice(0, -1).join('/');
      if (this.allDirectories.includes(parent)) {
        this.$emit('setCurrentDir', {
          locationType: this.locationType,
          dirName: parent,
        });
      } else {
        console.error(parent, 'not found');
      }
    },
    createFolder() {
      console.log('create folder');
    },
  },
  computed: {
    headers() {
      const headers = this.availableHeaders.filter((h) =>
        this.columnsShown.includes(h.value)
      );
      headers.push({
        text: '...',
        align: 'end',
        value: 'add_column',
        width: 20,
        sortable: false,
      });
      return headers;
    },
    tableItems() {
      const tableItems = this.dirContents.map((item) => {
        if (item.type === 'group' && item.name === this.expandedGroup) {
          return [
            item,
            ...item.files.map((file) =>
              Object.assign(file, { class: 'group-items' })
            ),
          ];
        }
        return item;
      });
      return tableItems.flat();
    },
  },
  data() {
    const availableHeaders = [
      {
        text: 'Filename',
        align: 'start',
        value: 'name',
        width: 200,
        sortable: true,
      },
      { text: 'Type', align: 'end', value: 'type' },
      { text: 'Size', align: 'end', value: 'size' },
      { text: 'Date Modified', align: 'end', value: 'modified' },
      { text: 'Owner', align: 'end', value: 'owner' },
    ];
    const columnsShown = ['name', 'type', 'size', 'modified'];

    return {
      showColumnPicker: false,
      filterString: undefined,
      selectedItems: [],
      expandedGroup: undefined,
      availableHeaders,
      columnsShown,
    };
  },
};
</script>

<template>
  <v-card>
    <div class="dir-select-box">
      <v-select
        :items="allDirectories"
        :value="currentDir"
        :label="locationType + ' Directory'"
        class="dir-select"
        solo
        hide-details
        @change="
          (dir) => this.$emit('setCurrentDir', { locationType, dirName: dir })
        "
      />
      <v-btn x-small style="height: 45px" @click="goBack">
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>
      <v-btn x-small style="height: 45px" @click="goForward">
        <v-icon>mdi-arrow-right</v-icon>
      </v-btn>
      <v-btn x-small style="height: 45px" @click="goToParent">
        <v-icon>mdi-folder-arrow-up-outline</v-icon>
      </v-btn>

      <v-btn
        x-small
        style="height: 45px; margin-left: 10px"
        @click="createFolder"
      >
        <v-icon>mdi-folder-plus-outline</v-icon>
      </v-btn>
    </div>

    <div class="filter-box">
      <v-chip
        color="rgb(70, 70, 70)"
        small
        class="filter-button"
        text-color="white"
      >
        <v-avatar>
          <v-icon :small="small">mdi-history</v-icon>
        </v-avatar>
        <div v-if="!small" class="pl-1">Recents</div>
      </v-chip>
      <v-chip
        color="rgb(70, 70, 70)"
        small
        class="filter-button"
        text-color="white"
      >
        <v-avatar>
          <v-icon :small="small">mdi-heart</v-icon>
        </v-avatar>
        <div v-if="!small" class="pl-1">Favorites</div>
      </v-chip>
      <v-chip
        color="rgb(70, 70, 70)"
        small
        class="filter-button"
        text-color="white"
      >
        <v-avatar>
          <v-icon :small="small">mdi-folder-marker</v-icon>
        </v-avatar>
        <div v-if="!small" class="pl-1">Locations</div>
      </v-chip>
      <v-text-field
        v-model="filterString"
        prepend-icon="mdi-magnify"
        hide-details
        autofocus
        placeholder="Filter by keyword"
        class="filter-input"
      />
    </div>
    <div style="position: relative">
      <v-data-table
        show-select
        hide-default-footer
        fixed-header
        v-model="selectedItems"
        :items="tableItems"
        item-key="name"
        item-class="class"
        :headers="headers"
        :search="filterString"
        @item-selected="selectItem"
        @dblclick:row="openItem"
      >
        <template v-slot:[`header.add_column`]="{}">
          <v-btn x-small depressed @click="showColumnPicker = true">
            <v-icon>mdi-dots-horizontal</v-icon>
          </v-btn>
        </template>
        <template v-slot:[`item.name`]="{ item }">
          <v-icon v-if="item.type === 'group'" @click="() => expandGroup(item)">
            {{ expandedGroup === item.name ? 'mdi-menu-up' : 'mdi-menu-down' }}
          </v-icon>
          <v-icon v-else>{{ getIcon(item.type) }}</v-icon>
          {{ item.name }}
        </template>
      </v-data-table>
      <v-overlay
        absolute
        :value="showColumnPicker"
        @click="showColumnPicker = false"
      >
        <v-card @click.stop light class="pa-3 column-picker">
          <v-card-subtitle class="py-1">Column Visibility</v-card-subtitle>
          <v-checkbox
            v-for="availableHeader in availableHeaders"
            v-model="columnsShown"
            :key="availableHeader.value"
            :value="availableHeader.value"
            :label="availableHeader.text"
            dense
            hide-details
          />
        </v-card>
      </v-overlay>
    </div>
  </v-card>
</template>

<style scoped>
.dir-select-box {
  padding: 10px 15px;
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  row-gap: 10px;
  background-color: lightgrey;
}
.dir-select {
  margin-right: 10px;
  min-width: 200px;
  max-width: 650px;
  background-color: white;
}
.filter-box {
  background-color: rgb(70, 70, 70);
  color: white;
  padding: 10px 15px;
  display: flex;
  align-items: center;
}
.filter-button {
  outline: 1px solid white;
  color: white;
  padding: 0px 5px;
  margin: 0px 3px;
  min-width: 32px;
}
.filter-input {
  background-color: white;
  height: 30px;
  border-radius: 20px;
  padding: 0px 10px;
  min-width: 20px;
  margin-top: 0;
  margin-left: 5px;
}
.column-picker {
  right: 10px;
  top: 10px;
  width: 300px;
  position: absolute;
}
.group-items {
  background-color: gray;
}
</style>

<style>
.v-overlay__content {
  width: 100%;
  height: 100%;
}
</style>
