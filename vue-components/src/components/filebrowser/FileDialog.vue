<script lang="ts">
import FileBrowser from './FileBrowser.vue';
export default {
  components: { FileBrowser },
  props: {
    mode: {
      type: String,
      default: 'Save',
    },
    dark: {
      type: Boolean,
      default: false,
    },
    localDirectories: {
      type: Array,
      default: () => [],
    },
    remoteDirectories: {
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
  },
  data() {
    return {
      dialogOpen: false,
      syncCurrentLocalAndRemote: false,
      unsyncedCurrentTab: 'local',
      filename: undefined,
      filetype: this.fileTypes[0]?.value,
      currentSelected: [],
    };
  },
  methods: {
    submit() {
      this.$emit('submit', {
        mode: this.mode,
        filename: this.filename + this.filetype,
      });
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
    <v-btn color="primary" @click="dialogOpen = true"> {{ mode }} </v-btn>
    <v-dialog
      v-model="dialogOpen"
      transition="dialog-bottom-transition"
      max-width="800"
    >
      <v-card>
        <v-card-text class="text-h6 grey lighten-2">
          {{ mode }}
          <v-icon
            @click="dialogOpen = false"
            style="float: right; height: 30px"
          >
            mdi-close
          </v-icon>
        </v-card-text>
        <v-divider></v-divider>

        <v-btn
          fab
          small
          class="sync-button"
          :color="syncCurrentLocalAndRemote ? 'primary' : ''"
          @click="syncCurrentLocalAndRemote = !syncCurrentLocalAndRemote"
        >
          <v-icon>mdi-folder-sync-outline</v-icon>
        </v-btn>
        <div v-if="!syncCurrentLocalAndRemote">
          <v-tabs
            grow
            v-model="unsyncedCurrentTab"
            active-class="highlighted-tab"
          >
            <v-tab>Local</v-tab>
            <v-tab>Remote</v-tab>
          </v-tabs>
          <v-tabs-items v-model="unsyncedCurrentTab">
            <v-tab-item>
              <file-browser
                @setCurrentDir="setCurrentDir"
                @setCurrentSelected="setCurrentSelected"
                @setFileName="(name) => (this.filename = name)"
                locationType="Local"
                :small="syncCurrentLocalAndRemote"
                :allDirectories="localDirectories"
                :currentDir="currentLocalDir"
                :dirContents="currentLocalDirContents"
              />
            </v-tab-item>
            <v-tab-item>
              <file-browser
                @setCurrentDir="setCurrentDir"
                @setCurrentSelected="setCurrentSelected"
                @setFileName="(name) => (this.filename = name)"
                locationType="Remote"
                :small="syncCurrentLocalAndRemote"
                :allDirectories="remoteDirectories"
                :currentDir="currentRemoteDir"
                :dirContents="currentRemoteDirContents"
              />
            </v-tab-item>
          </v-tabs-items>
        </div>
        <div v-else class="sync-display">
          <div>
            <v-tabs grow>
              <v-tab class="highlighted-tab">Local</v-tab>
            </v-tabs>
            <file-browser
              @setCurrentDir="setCurrentDir"
              @setCurrentSelected="setCurrentSelected"
              @setFileName="(name) => (this.filename = name)"
              locationType="Local"
              :small="syncCurrentLocalAndRemote"
              :allDirectories="localDirectories"
              :currentDir="currentLocalDir"
              :dirContents="currentLocalDirContents"
            />
          </div>
          <div>
            <v-tabs grow>
              <v-tab class="highlighted-tab">Remote</v-tab>
            </v-tabs>
            <file-browser
              @setCurrentDir="setCurrentDir"
              @setCurrentSelected="setCurrentSelected"
              @setFileName="(name) => (this.filename = name)"
              locationType="Remote"
              :small="syncCurrentLocalAndRemote"
              :allDirectories="remoteDirectories"
              :currentDir="currentRemoteDir"
              :dirContents="currentRemoteDirContents"
            />
          </div>
        </div>
        <div class="pa-3 container">
          <v-btn
            v-if="mode === 'Open'"
            :disabled="currentSelected.length < 1"
            @click="submit"
          >
            {{
              currentSelected.length > 1
                ? 'Open multiple as time series'
                : 'Open'
            }}
          </v-btn>
          <div v-if="mode === 'Save'" class="container">
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
            <v-btn :disabled="!(filename && filetype)" @click="submit">
              {{ mode }}
            </v-btn>
          </div>
        </div>
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
