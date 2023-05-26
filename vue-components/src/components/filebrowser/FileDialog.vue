<script lang="ts">
import DirBrowser from './DirBrowser.vue';
export default {
  components: { DirBrowser },
  props: {
    title: {
      type: String,
      default: 'File browser',
    },
    locations: {
      type: String,
      default: 'local', // local, remote, both, both-with-sync
    },
    gotoShortcuts: {
      type: Array,
      default: () => ['favorites', 'recents', 'locations'],
    },
    mode: {
      type: String,
      default: 'open', // open, save, ...
    },
    enableHistory: {
      type: Boolean,
    },
    visible: {
      type: Boolean,
    },
    dark: {
      type: Boolean,
      default: false,
    },
    localHierarchy: {
      type: Array,
      default: () => [],
    },
    remoteHierarchy: {
      type: Array,
      default: () => [],
    },
    currentLocalDir: {
      type: String,
      default: undefined,
    },
    currentRemoteDir: {
      type: String,
      default: undefined,
    },
    currentLocalDirContents: {
      type: Array,
      default: () => [],
    },
    currentRemoteDirContents: {
      type: Array,
      default: () => [],
    },
    fileTypes: {
      type: Array,
      default: () => [],
    },
    byteFormatter: {
      type: Function,
      required: false,
      default: (bytes) => bytes + ' B',
    },
    dateFormatter: {
      type: Function,
      required: false,
      default: (timestamp) => new Date(timestamp * 1000).toDateString(),
    },
  },
  data() {
    return {
      locationSelector: 0,
      syncCurrentLocalAndRemote: false,
      filename: undefined,
      filetype: this.fileTypes[0]?.value,
      currentSelected: [],
    };
  },
  computed: {
    showLocationSelector() {
      return this.locations.includes('both');
    },
    showSyncLocation() {
      return this.locations.includes('-with-sync');
    },
    showLocal() {
      if (this.showSyncLocation) {
        return this.locationSelector === 0;
      }
      return this.locations === 'local';
    },
    showRemote() {
      if (this.showSyncLocation) {
        return this.locationSelector === 1;
      }
      return this.locations === 'remote';
    },
  },
  methods: {
    submit() {
      this.$emit('submit', {
        currentSelected: this.currentSelected,
        filename: this.filename,
        filetype: this.filetype,
        location: this.locations,
      });
    },
    close() {
      this.$emit('close');
    },
    setCurrentDir({ locationType, dirName }) {
      if (locationType === 'Local') {
        this.$emit('setLocalDir', dirName);
      } else {
        this.$emit('setRemoteDir', dirName);
      }
    },
    setCurrentSelected(selected) {
      this.currentSelected = selected;
    },
  },
};
</script>

<template>
  <div class="container">
    <v-dialog
      :value="visible"
      transition="scroll-x-reverse-transition"
      fullscreen
    >
      <v-card class="fill-height" rounded="0">
        <v-card-title
          class="px-2 py-1 text-h6 grey darken-1 grey--text text--lighten-4"
          dense
        >
          {{ title }}
          <v-spacer />
          <v-icon color="grey lighten-4" @click="close">mdi-close</v-icon>
        </v-card-title>

        <v-card-text class="pa-0" style="height: calc(100% - 110px)">
          <v-btn
            v-if="showSyncLocation"
            fab
            small
            class="sync-button"
            :color="syncCurrentLocalAndRemote ? 'primary' : ''"
            @click="syncCurrentLocalAndRemote = !syncCurrentLocalAndRemote"
          >
            <v-icon>mdi-folder-sync-outline</v-icon>
          </v-btn>
          <div v-if="showLocationSelector && !syncCurrentLocalAndRemote">
            <v-tabs
              grow
              v-model="locationSelector"
              active-class="highlighted-tab"
            >
              <v-tab>Local</v-tab>
              <v-tab>Remote</v-tab>
            </v-tabs>
          </div>

          <dir-browser
            v-if="showLocal"
            @setCurrentDir="setCurrentDir"
            @setCurrentSelected="setCurrentSelected"
            @setFileName="filename = $event"
            @goto="$emit('goto', $event)"
            :gotoShortcuts="gotoShortcuts"
            :enableHistory="enableHistory"
            locationType="Local"
            :small="syncCurrentLocalAndRemote"
            :directoryHierarchy="localHierarchy"
            :currentDir="currentLocalDir"
            :dirContents="currentLocalDirContents"
            :byteFormatter="byteFormatter"
            :dateFormatter="dateFormatter"
            :canCreateDirectory="mode === 'save'"
          />
          <dir-browser
            v-if="showRemote"
            @setCurrentDir="setCurrentDir"
            @setCurrentSelected="setCurrentSelected"
            @setFileName="filename = $event"
            @goto="$emit('goto', $event)"
            :gotoShortcuts="gotoShortcuts"
            :enableHistory="enableHistory"
            locationType="Remote"
            :small="syncCurrentLocalAndRemote"
            :directoryHierarchy="remoteHierarchy"
            :currentDir="currentRemoteDir"
            :dirContents="currentRemoteDirContents"
            :byteFormatter="byteFormatter"
            :dateFormatter="dateFormatter"
            :canCreateDirectory="mode === 'save'"
          />
        </v-card-text>
        <v-row class="pa-3 mx-0 my-2">
          <v-btn
            v-if="mode === 'open'"
            color="grey darken-1 grey--text text--lighten-3"
            :disabled="currentSelected.length < 1"
            @click="submit"
          >
            {{ currentSelected.length > 1 ? 'Open group' : 'Open' }}
          </v-btn>
          <div v-if="mode === 'save'">
            <v-text-field
              v-model="filename"
              autofocus
              placeholder="File name"
            />
            <v-select
              v-model="filetype"
              :items="fileTypes"
              label="File Type"
              class="dir-select"
              solo
            />
            <v-btn
              :disabled="!(filename && filetype)"
              @click="submit"
              color="grey darken-1 grey--text text--lighten-3"
            >
              Save
            </v-btn>
          </div>
          <v-spacer />
          <v-btn outlined @click="close">Cancel</v-btn>
        </v-row>
      </v-card>
    </v-dialog>
  </div>
</template>

<style scoped>
.container {
  display: flex;
  width: 100%;
  justify-content: space-around;
  align-items: baseline;
  column-gap: 10px;
  flex-wrap: wrap;
}
.sync-button {
  position: absolute;
  right: calc(50% - 20px);
  z-index: 1;
}
.sync-display {
  display: flex;
  width: 100%;
}
.sync-display > div {
  width: 50%;
}
.highlighted-tab {
  background-color: lightblue !important;
}
.v-dialog > .v-card > .v-card__text {
  padding: 5px 20px;
}
.dir-select {
  margin-right: 10px;
  min-width: 200px;
  max-width: 650px;
  background-color: white;
}
</style>
