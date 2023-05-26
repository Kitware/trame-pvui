<script lang="ts">
import components from '../../components';
const { FileBrowser } = components;

function addFiles(array, count = 100) {
  const type = 'file';
  const size = 100000;
  const modified = '10/30/22 12:23pm';
  const owner = 'root';

  for (let i = 0; i < count; i++) {
    array.push({
      name: `generated_${i}.txt`,
      type,
      size,
      modified,
      owner,
    });
  }
}

export default {
  name: 'HomePage',
  components: { FileBrowser },
  methods: {
    getDirContents(dir: string) {
      console.log('getting random contents for', dir);
      const possibleFiles = [
        {
          name: 'example1',
          type: 'file',
          size: '10KB',
          modified: '10/30/22 12:23pm',
          owner: 'root',
        },
        {
          name: 'example2',
          type: 'file',
          size: '20KB',
          modified: '10/30/22 2:00pm',
          owner: 'root',
        },
        {
          name: 'example3',
          type: 'file',
          size: '30KB',
          modified: '10/30/22 3:00pm',
          owner: 'root',
        },
        {
          name: 'a big file',
          type: 'file',
          size: '10MB',
          modified: '10/31/22 10:00pm',
          owner: 'root',
        },
        {
          name: 'foo',
          type: 'file',
          size: '1MB',
          modified: '10/29/22 4:00pm',
          owner: 'root',
        },
        {
          name: 'bar',
          type: 'file',
          size: '1MB',
          modified: '10/29/22 4:00pm',
          owner: 'root',
        },
        {
          name: 'One',
          type: 'folder',
          size: '--',
          modified: '10/29/22 4:00pm',
          owner: 'root',
        },
        {
          name: 'Two',
          type: 'folder',
          size: '--',
          modified: '10/29/22 4:00pm',
          owner: 'root',
        },
        {
          name: 'Group set',
          type: 'group',
          size: '--',
          modified: '--',
          owner: 'temp',
          files: [
            {
              name: 'Group file A',
              type: 'file',
              size: '2MB',
              modified: '11/01/22 8:00am',
              owner: 'temp',
            },
            {
              name: 'Group file B',
              type: 'file',
              size: '2MB',
              modified: '11/01/22 8:00am',
              owner: 'temp',
            },
            {
              name: 'Group file C',
              type: 'file',
              size: '2MB',
              modified: '11/01/22 8:00am',
              owner: 'temp',
            },
          ],
        },
      ];
      addFiles(possibleFiles, 100);
      return possibleFiles.filter(() => Math.random() < 0.8);
    },
    save(fileInfo) {
      console.log('save', fileInfo);
    },
    open(fileInfo) {
      console.log('save', fileInfo);
    },
  },
  computed: {
    currentLocalDirContents() {
      return this.getDirContents(this.currentLocalDir);
    },
    currentRemoteDirContents() {
      return this.getDirContents(this.currentRemoteDir);
    },
  },
  data() {
    return {
      localDirectories: [
        '/home/localUser/Data',
        '/home/localUser/Data/One',
        '/home/localUser/Data/Two',
        '/home/localUser/Data/Three',
        '/home/localUser/Downloads',
        '/home/localUser/Downloads/One',
        '/home/localUser/Downloads/Two',
        '/home/localUser/Downloads/Three',
      ],
      remoteDirectories: [
        'remote_host:/root/data',
        'remote_host:/root/data/One',
        'remote_host:/root/data/Two',
        'remote_host:/root/data/Three',
      ],
      currentLocalDir: '/home/localUser/Data/One',
      currentRemoteDir: 'remote_host:/root/data/one',
      fileTypes: [
        {
          value: '.vtpd',
          text: 'VTK PartitionedDataSetCollection File (*.vtpd)',
        },
      ],
    };
  },
};
</script>

<template>
  <div id="app">
    <v-app>
      <div class="d-flex">
        <file-browser
          visible
          title="Save State"
          mode="save"
          :currentLocalDir="currentLocalDir"
          :currentRemoteDir="currentRemoteDir"
          :remoteDirectories="remoteDirectories"
          :localDirectories="localDirectories"
          :currentLocalDirContents="currentLocalDirContents"
          :currentRemoteDirContents="currentRemoteDirContents"
          :fileTypes="fileTypes"
          @setLocalDir="(dir) => (currentLocalDir = dir)"
          @setRemoteDir="(dir) => (currentRemoteDir = dir)"
          @submit="save"
        />
        <file-browser
          visible
          title="Open Data File"
          mode="open"
          :gotoShortcuts="['favorites', 'recents', 'locations']"
          :currentLocalDir="currentLocalDir"
          :currentRemoteDir="currentRemoteDir"
          :remoteDirectories="remoteDirectories"
          :localDirectories="localDirectories"
          :currentLocalDirContents="currentLocalDirContents"
          :currentRemoteDirContents="currentRemoteDirContents"
          :fileTypes="fileTypes"
          @setLocalDir="(dir) => (currentLocalDir = dir)"
          @setRemoteDir="(dir) => (currentRemoteDir = dir)"
          @submit="open"
        />
      </div>
    </v-app>
  </div>
</template>
