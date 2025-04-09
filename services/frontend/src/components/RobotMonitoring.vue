<template>
  <div class="bg-gray-50 rounded-lg p-4 shadow-md">
    <h2 class="text-xl font-semibold mb-4">Monitoring</h2>
    <div class="bg-white rounded-lg border border-gray-200 p-4">
      <div class="flex flex-col lg:flex-row space-y-4 lg:space-y-0 lg:space-x-4">
        <div class="flex flex-col w-full lg:w-1/2 space-y-14">
          <ConnectionInfoCard :connectionState="connectionState" />
          <RobotStatusCard :robotStatus="robotState.status" />
          <UptimeCard :robotUptime="robotState.uptime"/>
        </div>
        <div class="flex flex-col sm:flex-row w-full space-y-4 md:space-y- lg:space-y-0 sm:space-x-4 mt-4">
          <div class="w-full sm:w-1/3">
            <Thermometer :temperatureValue="robotState.temperature ?? 0" />
          </div>
          <div class="w-full sm:w-1/3">
            <Battery :powerWatts="robotState.power_consumption ?? 0" />
          </div>
          <div class="w-full sm:w-1/3">
            <Fan :speed="robotState.fan_speed" :mode="robotState.fan_mode"/>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import Fan from "@/components/css/Fan.vue";
import Battery from "@/components/css/Battery.vue";
import Thermometer from "@/components/css/Thermometer.vue";
import UptimeCard from "@/components/Cards/UptimeCard.vue";
import RobotStatusCard from "@/components/Cards/RobotStatusCard.vue";
import ConnectionInfoCard from "@/components/Cards/ConnectionInfoCard.vue";

interface LogEntry {
  timestamp: string;
  message: string;
}

interface RobotState {
  status: string;
  temperature: number | null;
  power_consumption: number | null;
  fan_speed: number;
  fan_mode: string;
  static_fan_speed: number;
  uptime: string;
  logs: LogEntry[];
}

defineProps<{
  connectionState: string;
  robotState: RobotState;
}>();
</script>