<template>
  <div class="col-span-1 h-full bg-white p-6 rounded-lg shadow-lg space-y-6 flex flex-col justify-center items-center">
    <div class="graphic-wrapper">
      <div :class="['battery-icon_wrapper', powerColorClass]">
        <div
            v-for="index in 5"
            :key="index"
            :class="['battery-icon_ind', { filled: index <= filledBars }]"
        ></div>
      </div>
    </div>

    <div class="text-wrapper">
      <p :class="powerColorClass"></p>
      <p> Power Consumption </p>
    </div>
    {{ powerWatts }}W
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  powerWatts: {
    type: Number,
    required: true,
    default: 0,
    validator(value: number) {
      return value >= 0;
    },
  },
  maxPowerThreshold: {
    type: Number,
    default: 25,
  },
});

// Computed properties
const powerPercentage = computed(() => {
  return Math.min(100, (props.powerWatts / props.maxPowerThreshold) * 100);
});

const filledBars = computed(() => {
  return Math.ceil(powerPercentage.value / 20);
});

const powerColorClass = computed(() => {
  if (powerPercentage.value <= 40) {
    return "lvl3";
  } else if (powerPercentage.value <= 80) {
    return "lvl2";
  } else {
    return "lvl1";
  }
});
</script>

<style scoped lang="scss">
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

.graphic-wrapper {
  margin-top: 100px;
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
}

.battery-icon_wrapper {
  --width: 90px;
  --gap: calc(var(--width) / 15);
  --border-r: calc(var(--width) / 22.5);

  width: var(--width);
  aspect-ratio: 0.55;
  border: var(--gap) solid #161A1D;
  border-radius: var(--border-r);
  padding: var(--gap);
  display: grid;
  grid-template-rows: repeat(5, 1fr);
  gap: var(--gap);
  position: relative;
}

.battery-icon_wrapper:before {
  content: "";
  position: absolute;
  background: #161A1D;
  border-radius: var(--border-r);
  width: calc(var(--width) / 2);
  aspect-ratio: 3;
  top: calc((var(--width) / 6) * -1);
  left: 50%;
  transform: translateX(-50%);
}

.battery-icon_ind {
  background: transparent;
}

.battery-icon_wrapper.lvl1 {
  --bg-color: #df0012;
}

.battery-icon_wrapper.lvl2 {
  --bg-color: #fbb103;
}

.battery-icon_wrapper.lvl3 {
  --bg-color: #51af27;
}

.battery-icon_ind.filled {
  background: var(--bg-color);
}

.text-wrapper {
  margin-top: 120px;
  display: flex;
  justify-content: center;
}

.text-wrapper p {
  display: flex;
  align-items: center;
  position: relative;
  font-weight: bold;
  font-size: 1.1rem;
  padding-left: 10px;
}

p:before {
  content: "";
  position: absolute;
  width: 10px;
  height: 10px;
  left: 0;
}

p.lvl1 {
  color: #df0012;
}

p.lvl2 {
  color: #fbb103;
}

p.lvl3 {
  color: #51af27;
}

p.lvl1:before {
  background: #df0012;
}

p.lvl2:before {
  background: #fbb103;
}

p.lvl3:before {
  background: #51af27;
}
</style>