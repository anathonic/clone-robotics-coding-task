<template>
  <div class="col-span-1 bg-white p-6 rounded-lg shadow-lg space-y-6">
    <h1 class="text-xl font-semibold tracking-wider text-left text-gray-700 uppercase mb-4">
      Uptime
    </h1>
    <div class="flex items-center space-x-5">
      <p class="text-lg font-medium tracking-wide text-gray-600 mt-4">
        {{ robotUptime }}
      </p>
    </div>
  </div>
</template>

<script setup lang="ts">
defineProps({
  robotUptime: {
    type: String,
    required: true,
  },
});
</script>