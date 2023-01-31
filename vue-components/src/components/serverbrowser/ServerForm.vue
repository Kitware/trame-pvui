<script lang="ts">
import { Server, ServerType } from './schema';

const startupPlaceholder =
  'Execute an external command to start the server. Leave blank to use the default startup configuration.';

export default {
  props: {
    server: {
      type: Object as () => Server | null,
      default: null,
    },
  },
  data() {
    const server = this.server || {
      name: '',
      host: '',
      port: 11111,
      type: ServerType.ClientServer,
      startupCommand: '',
      waitTime: 0,
    };
    return {
      ...server,
      serverTypes: Object.values(ServerType),
      startupPlaceholder,
    };
  },
  watch: {
    server() {
      const server = this.server;
      this.name = server ? server.name : '';
      this.host = server ? server.host : '';
      this.port = server ? server.port : 11111;
      this.type = server ? server.type : ServerType.ClientServer;
      this.startupCommand = server ? server.startupCommand : '';
      this.waitTime = server ? server.waitTime : 0;
    },
  },
  methods: {
    save() {
      this.$emit('save', {
        name: this.name,
        host: this.host,
        port: this.port,
        type: this.type,
        startupCommand: this.startupCommand,
        waitTime: this.waitTime,
      });
    },
  },
};
</script>

<template>
  <v-card class="pt-2" dark>
    <v-container>
      <v-row>
        <v-col cols="6">
          <v-text-field
            outlined
            hide-details
            label="Name"
            v-model="name"
            persistent-placeholder
            dense
          />
        </v-col>
        <v-col cols="6">
          <v-select
            :items="serverTypes"
            label="Server Type"
            outlined
            dense
            hide-details
            v-model="type"
          />
        </v-col>
      </v-row>
      <v-row align="center">
        <v-divider />
        <div class="mx-1 text-uppercase subtitle-1">Client / server</div>
        <v-divider />
      </v-row>
      <v-row>
        <v-col cols="8">
          <v-text-field
            outlined
            hide-details
            label="Host"
            persistent-placeholder
            v-model="host"
            dense
          />
        </v-col>
        <v-col cols="4">
          <v-text-field
            type="number"
            outlined
            hide-details
            label="Port"
            v-model="port"
            dense
          />
        </v-col>
      </v-row>
      <v-row><v-divider class="my-2" /></v-row>
      <v-row>
        <v-col cols="6">
          <v-textarea
            outlined
            label="Startup Command"
            v-model="startupCommand"
            :placeholder="startupPlaceholder"
            persistent-placeholder
          />
        </v-col>
        <v-col cols="2">
          <v-text-field
            type="number"
            outlined
            hide-details
            label="Seconds"
            v-model="waitTime"
            dense
          />
        </v-col>
        <v-col>
          <div class="subtitle-2">
            Specify how long to wait before connecting after the startup command
            is executed.
          </div>
          <div class="caption grey--text">
            Leave at 0 if you do not wish to wait.
          </div>
        </v-col>
      </v-row>
    </v-container>
    <v-toolbar>
      <v-btn @click="$emit('close')" color="secondary">Cancel</v-btn>
      <v-spacer />
      <v-btn @click="save" class="pl-2" color="primary">
        <v-icon class="mr-1">mdi-content-save</v-icon>
        Save
      </v-btn>
    </v-toolbar>
  </v-card>
</template>
