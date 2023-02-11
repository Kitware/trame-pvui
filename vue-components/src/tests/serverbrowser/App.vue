<script lang="ts">
import { defineComponent, ref } from 'vue';
import components from '../../components';
import { Server } from '../../components/serverbrowser/schema';
const { ServerBrowser } = components;

export default defineComponent({
  name: 'HomePage',
  components: { ServerBrowser },
  setup() {
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
