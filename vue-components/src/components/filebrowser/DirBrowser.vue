<script lang="ts">
export default {
  props: {
    enableHistory: {
      type: Boolean,
    },
    locationType: {
      type: String,
      required: true,
    },
    small: {
      type: Boolean,
      default: true,
    },
    directoryHierarchy: {
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
    byteFormatter: {
      type: Function,
      required: false,
      default: (bytes) => bytes,
    },
    dateFormatter: {
      type: Function,
      required: false,
      default: (timestamp) => timestamp,
    },
    gotoShortcuts: {
      type: Array,
      default: () => ['favorites', 'recents', 'locations'],
    },
    canCreateDirectory: {
      type: Boolean,
    },
  },
  methods: {
    getIcon(type: string) {
      switch (type) {
        case 'folder':
          return 'mdi-folder';
        default:
          return 'mdi-file-outline';
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
        this.filterString = '';
        this.$emit('setCurrentDir', {
          locationType: this.locationType,
          dirName: item.full_path,
        });
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
    goToLocations() {
      this.$emit('goto', 'locations');
    },
    goToRecents() {
      this.$emit('goto', 'recents');
    },
    goToFavorites() {
      this.$emit('goto', 'favorites');
    },
    goToParent() {
      // TODO this will fail with a windows server
      const parent = this.currentDir.split('/').slice(0, -1).join('/');
      this.$emit('setCurrentDir', {
        locationType: this.locationType,
        dirName: parent,
      });
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
        sortable: true,
      },
      { text: 'Type', width: 50, align: 'center', value: 'type' },
      { text: 'Size', width: 120, align: 'end', value: 'size' },
      {
        text: 'Date Modified',
        width: 200,
        align: 'center',
        value: 'modification_time',
      },
      { text: 'Owner', width: 100, align: 'end', value: 'owner' },
    ];
    const columnsShown = ['name', 'type', 'size', 'modification_time'];

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
  <v-card class="fill-height" flat rounded="0">
    <div class="dir-select-box">
      <v-btn
        v-if="enableHistory"
        x-small
        width="35"
        height="35"
        class="mr-1"
        @click="goBack"
      >
        <v-icon>mdi-arrow-left</v-icon>
      </v-btn>

      <v-btn
        v-if="enableHistory"
        x-small
        width="35"
        height="35"
        class="mr-1"
        @click="goForward"
      >
        <v-icon>mdi-arrow-right</v-icon>
      </v-btn>

      <v-btn x-small width="35" height="35" class="mx-1" @click="goToParent">
        <v-icon>mdi-folder-arrow-up-outline</v-icon>
      </v-btn>

      <v-select
        dense
        :items="directoryHierarchy"
        :value="currentDir"
        :label="locationType + ' Directory'"
        class="mx-1"
        solo
        hide-details
        @change="
          (dir) => this.$emit('setCurrentDir', { locationType, dirName: dir })
        "
      />

      <v-btn
        v-if="canCreateDirectory"
        x-small
        width="35"
        height="35"
        class="ml-2"
        @click="createFolder"
      >
        <v-icon>mdi-folder-plus-outline</v-icon>
      </v-btn>
    </div>

    <div class="filter-box">
      <v-chip
        color="rgb(70, 70, 70)"
        small
        class="filter-button mr-2 px-1"
        @click="goToRecents"
        v-if="gotoShortcuts.includes('recents')"
      >
        <v-avatar>
          <v-icon small>mdi-history</v-icon>
        </v-avatar>
        <div v-if="!small" class="pr-1">Recents</div>
      </v-chip>
      <v-chip
        color="rgb(70, 70, 70)"
        small
        class="filter-button mr-2 px-1"
        @click="goToFavorites"
        v-if="gotoShortcuts.includes('favorites')"
      >
        <v-avatar>
          <v-icon small>mdi-heart</v-icon>
        </v-avatar>
        <div v-if="!small" class="pr-1">Favorites</div>
      </v-chip>
      <v-chip
        color="rgb(70, 70, 70)"
        small
        class="filter-button mr-2 px-1"
        @click="goToLocations"
        v-if="gotoShortcuts.includes('locations')"
      >
        <v-avatar>
          <v-icon small>mdi-folder-marker</v-icon>
        </v-avatar>
        <div v-if="!small" class="pr-1">Locations</div>
      </v-chip>
      <v-text-field
        v-model="filterString"
        prepend-inner-icon="mdi-magnify"
        clearable
        outlined
        filled
        rounded
        dense
        background-color="white"
        hide-details
        placeholder="Filter by keyword"
        style="transform: scale(0.75) translateX(15%)"
      />
    </div>

    <div
      style="
        position: relative;
        overflow: auto;
        height: calc(100% - 50px - 58px);
      "
    >
      <v-data-table
        show-select
        hide-default-footer
        fixed-header
        :itemsPerPage="-1"
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
        <template v-slot:[`item.size`]="{ item }">
          {{ byteFormatter(item.size) }}
        </template>
        <template v-slot:[`item.modification_time`]="{ item }">
          {{ dateFormatter(item.modification_time) }}
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
