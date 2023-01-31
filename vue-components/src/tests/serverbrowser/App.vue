<script lang="ts">
import { defineComponent, ref } from 'vue';
import { ServerBrowser } from '../../components';
import { Server } from '../../components/serverbrowser/schema';

export default defineComponent({
  name: 'HomePage',
  components: { ServerBrowser },
  setup() {
    // @zach: replaced reactive with ref due to the following warning:
    // [Vue warn]: Avoid using Array as root value for reactive()
    // as it cannot be tracked in watch() or watchEffect(). Use ref() instead. This is a Vue-2-only limitation.
    const servers = ref<Server[]>([]);

    function addServer(server: Server) {
      servers.value.splice(0, 0, server);
    }

    function updateServer(oldServer: Server, newServer: Server) {
      for (const i in servers) {
        if (servers[i].name === oldServer.name) {
          servers[i].name = newServer.name;
          servers[i].host = newServer.host;
          servers[i].port = newServer.port;
          servers[i].type = newServer.type;
          servers[i].startupCommand = newServer.startupCommand;
          servers[i].waitTime = newServer.waitTime;
          break;
        }
      }
    }

    return {
      servers,
      addServer,
      updateServer,
    };
  },
});
</script>

<template>
  <div id="app">
    <v-app>
      <server-browser
        :servers="servers"
        @add="addServer"
        @update="updateServer"
      />
    </v-app>
  </div>
</template>

<style scoped>
.container-1 {
  margin: 10px;
  padding: 10px;
  width: 400px;
  background-color: black;
}
.container-2 {
  margin: 10px;
  padding: 10px;
  border: 1px dashed black;
  width: 700px;
}
</style>
