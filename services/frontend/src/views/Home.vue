<template>
  <div class="home-view">
    <div class="w-full h-full bg-gray-100 px-8 py-6">
      <RobotMonitor :robot-state="robotState" :connection-state="connectionStatus" />
      <div class="control-panel py-6 ">
        <RobotControls
            :robot-state="robotState"
            @toggle-power="togglePower"
            @reset-robot="resetRobot"
            @set-fan-mode="setFanMode"
        />
      </div>
      <div class="logs-panel py-6">
        <RobotLogs :logs="robotState.logs || []" />
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, onBeforeUnmount } from 'vue';
import { eventService } from '../services/eventService';
import { connectWebSocket, closeWebSocket, connectionStatus, robotState } from '../services/wsService';

import RobotLogs from "@/components/RobotLogs.vue";
import RobotMonitor from "@/components/RobotMonitoring.vue";
import RobotControls from "@/components/RobotControl.vue";

const togglePower = async () => {
  await eventService.togglePower();
};

const resetRobot = async () => {
  await eventService.resetRobot();
};

const setFanMode = async (mode: string, staticValue?: number) => {
  await eventService.setFanMode(mode, staticValue);
};

const fetchInitialState = async () => {
  await eventService.fetchInitialState(robotState);
};

onMounted(() => {
  fetchInitialState();
  connectWebSocket();
});

onBeforeUnmount(() => {
  closeWebSocket();
});
</script>
