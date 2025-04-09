<template>
  <div class="robot-logs bg-gray-50 rounded-lg p-4 shadow-md">
    <h2 class="text-xl font-semibold mb-4">Robot Logs</h2>

    <div class="logs-container bg-gray-800 rounded-lg p-2 max-h-72 overflow-y-auto font-mono">
      <div v-if="logs.length === 0" class="no-logs text-gray-400 p-4 text-center">
        No logs available
      </div>

      <div v-else class="logs-list flex flex-col gap-1">
        <div
            v-for="(log, index) in logs"
            :key="index"
            class="log-entry flex p-2 rounded-md gap-3 text-sm text-gray-100 items-center"
            :class="`log-${log.level}`"
        >
          <div class="log-timestamp text-gray-400 flex-shrink-0">{{ formatTimestamp(log.timestamp) }}</div>
          <div class="log-level font-bold w-20 flex-shrink-0">{{ log.level.toUpperCase() }}</div>
          <div class="log-message flex-grow">{{ log.message }}</div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">

interface LogEntry {
  message: string;
  level: string;
  timestamp: string;
}

defineProps<{
  logs: LogEntry[];
}>();

const formatTimestamp = (timestamp: string) => {
  try {
    const date = new Date(timestamp);
    return date.toLocaleTimeString();
  } catch (e) {
    return timestamp;
  }
};
</script>

<style scoped>
.robot-logs {
  background-color: #f8fafc;
  border-radius: 0.5rem;
  padding: 1rem;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

h2 {
  margin-top: 0;
  margin-bottom: 1rem;
  font-size: 1.25rem;
}

.logs-container {
  background-color: #0B090A;
  border-radius: 0.375rem;
  padding: 0.5rem;
  max-height: 300px;
  overflow-y: auto;
  font-family: monospace;
}

.no-logs {
  color: #FFFFFF;
  padding: 1rem;
  text-align: center;
}

.logs-list {
  display: flex;
  flex-direction: column;
  gap: 0.25rem;
}

.log-entry {
  display: flex;
  padding: 0.5rem;
  border-radius: 0.25rem;
  gap: 0.75rem;
  font-size: 0.875rem;
  color: #f1f5f9;
  align-items: center;
}

.log-info {
  background-color: #161A1D;
}

.log-warning {
  background-color: #F89C00;
}

.log-error {
  background-color: #A4161A;
}

.log-timestamp {
  color: #FFFFFF;
  flex-shrink: 0;
}

.log-level {
  font-weight: bold;
  width: 80px;
  flex-shrink: 0;
}

.log-message {
  flex-grow: 1;
}

.logs-container::-webkit-scrollbar {
  width: 8px;
}

.logs-container::-webkit-scrollbar-track {
  background: #B1A7A6;
  border-radius: 4px;
}

.logs-container::-webkit-scrollbar-thumb {
  background: #D3D3D3;
  border-radius: 4px;
}

.logs-container::-webkit-scrollbar-thumb:hover {
  background: #F5F3F4;
}
</style>