<template>
  <div class="col-span-1 bg-white p-6 rounded-lg shadow-lg space-y-6">
    <h1 class="text-xl font-semibold tracking-wider text-left text-gray-700 uppercase mb-4">
      Robot Status
    </h1>
    <div class="flex items-center space-x-5">
      <span class="relative flex h-10 w-10 mt-4">
        <span
            class="animate-ping absolute inline-flex h-full w-full rounded-full opacity-75"
            :class="statusClass"
        ></span>
        <span
            class="relative inline-flex rounded-full h-10 w-10"
            :class="statusClass"
        ></span>
      </span>
      <p class="text-lg font-medium tracking-wide text-gray-600 mt-4">
        {{ robotStatus.toUpperCase() }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  robotStatus: {
    type: String,
    required: true,
  },
});

const statusClass = computed(() => {
  const status = props.robotStatus;
  return {
    'bg-green-600': status === 'idle',
    'bg-yellow-500': status === 'running',
    'bg-red-800': status === 'error',
    'bg-gray-500': status === 'offline',
  };
});
</script>