<template>
  <div class="col-span-1 bg-white p-6 rounded-lg shadow-lg space-y-6">
    <h1 class="text-xl font-semibold tracking-wider text-left text-gray-900 uppercase mb-4">
      Server Status
    </h1>
    <div class="flex items-center space-x-5">
      <span class="relative flex h-10 w-10 mt-4">
        <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
            :class="getWebsocketConnectionState(connectionState) === 'connected' ? 'bg-green-500' :
                   getWebsocketConnectionState(connectionState) === 'connecting' ? 'bg-orange-400' : ''"
        ></span>
        <span
            class="relative inline-flex rounded-full h-10 w-10"
            :class="getWebsocketConnectionState(connectionState) === 'connected' ? 'bg-green-600' :
                   getWebsocketConnectionState(connectionState) === 'connecting' ? 'bg-orange-500' : 'bg-gray-200'"
        ></span>
      </span>
      <p class="text-lg font-medium tracking-wide text-gray-600 mt-4">
        {{ connectionState.toUpperCase() }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  connectionState: {
    type: String,
    required: true,
  },
});

const getWebsocketConnectionState = (state: string) => {
  if (state === 'connected') return 'connected';
  if (state === 'connecting') return 'connecting';
  if (state === 'disconnected') return 'disconnected';
  return '';
};
</script>