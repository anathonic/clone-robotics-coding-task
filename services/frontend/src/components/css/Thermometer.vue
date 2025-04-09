<template>
  <div class="col-span-1 h-full bg-white p-6 rounded-lg shadow-lg space-y-6 flex flex-col justify-center items-center">
    <div id="termometer" :style="termometerStyle">
      <div id="temperature" :style="{ height: temperatureHeight }" :data-value="temperatureData"></div>
      <div id="graduations"></div>
    </div>
    <div class="power-wrapper">
      <p>Temperature</p>
    </div>
    {{ temperatureValue }} C
  </div>
</template>

<script setup lang="ts">
import {computed, ref} from 'vue';
import type { CSSProperties } from 'vue';

const props = defineProps({
  temperatureValue: {
    type: Number,
    required: true
  },
});

const minTemp = ref(-20);
const maxTemp = ref(100);

const temperatureHeight = computed(() => {
  return `${((props.temperatureValue - minTemp.value) / (maxTemp.value - minTemp.value)) * 100}%`;
});

const temperatureData = computed(() => {
  return `${props.temperatureValue} °C`;
});

const termometerStyle = computed(() => {
  return {
    width: '25px',
    height: '240px',
    background: '#2f2f35',
    border: '9px solid #1e1e24',
    borderRadius: '20px',
    position: 'relative',
    marginBottom: '50px',
    zIndex: '1',
    transform: 'rotate(180deg)',
  } as CSSProperties;
});
</script>

<style scoped lang="scss">
@import url('https://fonts.googleapis.com/css?family=Jaldi&display=swap');

#wrapper {
  margin: auto;
  display: flex;
  flex-direction: column;
  align-items: center;
}

p {
  -webkit-user-select: none;
  -moz-user-select: none;
  -ms-user-select: none;
  user-select: none;
}

#info {
  opacity: 0.2;
  margin: 0;
  text-align: center;
}

#termometer {
  width: 25px;
  background: #2f2f35;
  height: 240px;
  position: relative;
  border-radius: 20px;
  z-index: 1;
  border: 9px solid #1e1e24;
  transform: rotate(180deg);
  margin-top: 40px;
}

#temperature {
  bottom: 0;
  background: #E5383B;
  width: 100%;
  border-radius: 20px;
  background-size: 100% 200px;
  transition: all 0.2s ease-in-out;
}

#playground {
  font-size: 1.1em;
}

.power-wrapper {
  margin-top: 50px;
  display: flex;
  justify-content: center;
}

.power-wrapper p {
  display: flex;
  align-items: center;
  position: relative;
  font-weight: bold;
  font-size: 1.1rem;
  padding-left: 10px;
}
</style>