<template>
  <div class="w-full bg-gray-100 border-t-1 px-8 py-6 flex justify-end">
    <div class="flex items-center">
      <span class="mr-2 ml-2 text-xs font-semibold"> Clone Robotics © {{ date }}</span>
      <img class="h-5 max-w-xs" src="../assets/png/clone-robotics-logo.png" alt="">
    </div>
  </div>
</template>

<script setup lang="ts">
const date: number = new Date().getFullYear();
</script>