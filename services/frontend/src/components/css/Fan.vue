<template>
  <div class="col-span-1 h-full bg-white p-6 rounded-lg shadow-lg space-y-6 flex flex-col justify-center items-center">
    <div class="fan">
      <div
          class="fan-blades"
          :style="{ animationDuration: fanSpeed + 's' }"
      >
        <span class="center"></span>
        <div class="blade"><span></span></div>
        <div class="blade"><span></span></div>
        <div class="blade"><span></span></div>
        <div class="blade"><span></span></div>
      </div>
    </div>

      <div class="flex-col text-center">
        <div class="text-wrapper">
          <p> Mode </p>
        </div>
        {{ mode }}
        <div class="text-wrapper">
          <p> Speed </p>
        </div>
        {{ speed }}%
      </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

interface Props {
  speed?: number;
  mode?: string;
}

const props = withDefaults(defineProps<Props>(), {
  speed: 0,
  mode: 'Off'
});

const fanSpeed = computed(() => {
  const speed = props.speed || 0;
  return (100 - speed) * 0.05 + 1;
});
</script>

<style scoped>
html {
  overflow: hidden;
}

body {
  display: flex;
  justify-content: center;
  align-items: center;
  width: 100vw;
  height: 100vh;
}

.fan {
  width: 300px;
  height: 300px;
  position: relative;
  z-index: 1;
}


.fan-blades {
  width: 150px;
  height: 150px;
  position: absolute;
  top: 40%;
  left: calc(50% - 75px);
  transform-origin: center center;
  z-index: 1;
  animation: rotate infinite linear;
}

.fan-blades .blade {
  position: absolute;
  width: 25px;
  height: 100%;
  left: 50%;
  transform: translateX(-50%);
  perspective: 500px;
  transform-style: preserve-3d;
}

.fan-blades .blade:nth-child(2) {
  transform: translateX(-50%) rotate(90deg);
}

.fan-blades .blade:nth-child(3) {
  transform: translateX(-50%) rotate(180deg);
}

.fan-blades .blade:nth-child(4) {
  transform: translateX(-50%) rotate(270deg);
}

.fan-blades .blade span {
  width: 100%;
  height: 200%;
  border-radius: 44px;
  background: #222;
  position: absolute;
  top: -66px;
  display: block;
  transform-style: preserve-3d;
  transform: rotateX(78deg);
  overflow: hidden;
}

.fan-blades .blade span::after {
  width: 50%;
  height: 100%;
  content: "";
  display: block;
  background: #333;
  transform: rotateX(0deg);
}

.fan-blades .center {
  position: absolute;
  overflow: hidden;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  left: 50%;
  top: 50%;
  transform: translate(-50%, -50%) rotate(45deg);
  background: #ccc;
  z-index: 2;
}

.fan-blades .center::after {
  content: "";
  width: 30px;
  height: 15px;
  background: #888;
  display: block;
}

.text-wrapper {
  margin-top: 30px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.text-wrapper p {
  display: flex;
  align-items: center;
  position: relative;
  font-weight: bold;
  font-size: 1.1rem;
}

@keyframes rotate {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}
</style>