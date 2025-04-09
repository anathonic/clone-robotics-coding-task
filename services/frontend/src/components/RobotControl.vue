<template>
  <div class="bg-gray-50 rounded-lg p-4 shadow-md">
    <h2 class="text-xl font-semibold mb-4">Control</h2>

    <div class="bg-white rounded-lg border border-gray-200 p-4">
      <div class="flex gap-4 mb-6">
        <button
            :class="['flex-1 py-3 px-4 rounded-md font-bold text-white transition-colors', powerButtonClass]"
            @click="handlePowerToggle"
            :disabled="robotState.status === 'offline'"
        >
          {{ powerButtonText }}
        </button>

        <button
            class="flex-1 py-3 px-4 rounded-md font-bold text-white bg-gray-900 hover:bg-gray-800 disabled:opacity-50"
            @click="handleReset"
            :disabled="!canReset"
        >
          Reset
        </button>
      </div>

      <div class="mt-4">
        <h3 class="text-lg font-medium mb-2">Fan Mode</h3>

        <div class="mb-4">
          <div class="flex gap-6">
            <label class="flex items-center gap-2 cursor-pointer">
              <input
                  type="radio"
                  name="fanMode"
                  value="proportional"
                  :checked="robotState.fan_mode === 'proportional'"
                  @change="handleFanModeChange('proportional')"
                  :disabled="robotState.status === 'offline'"
                  class="cursor-pointer custom-radio"
              />
              <span>Proportional</span>
            </label>

            <label class="flex items-center gap-2 cursor-pointer">
              <input
                  type="radio"
                  name="fanMode"
                  value="static"
                  :checked="robotState.fan_mode === 'static'"
                  @change="handleFanModeChange('static')"
                  :disabled="robotState.status === 'offline'"
                  class="cursor-pointer custom-radio"
              />
              <span>Static</span>
            </label>
          </div>
        </div>

        <div v-if="robotState.fan_mode === 'static'" class="mt-4">
          <label class="flex flex-col gap-2">
            <span class="text-lg font-medium mb-2">Fan Speed: {{ staticFanSpeed }}%</span>
            <input
                type="range"
                min="0"
                max="100"
                v-model="staticFanSpeed"
                @change="handleStaticFanSpeedChange"
                :disabled="robotState.status === 'offline'"
                class="w-full h-2 custom-range cursor-pointer disabled:opacity-50"
            />
          </label>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue';

interface RobotState {
  status: 'offline' | 'idle' | 'running' | 'error';
  fan_mode: 'static' | 'proportional';
  static_fan_speed: number | null;
}

const props = defineProps<{
  robotState: RobotState;
}>();

const emit = defineEmits<{
  (e: 'toggle-power'): void;
  (e: 'reset-robot'): void;
  (e: 'set-fan-mode', mode: string, fanSpeed?: number): void;
}>();

const staticFanSpeed = ref(props.robotState.static_fan_speed || 50);

watch(() => props.robotState.static_fan_speed, (newValue) => {
  if (newValue !== undefined && newValue !== null) {
    staticFanSpeed.value = newValue;
  }
});

const powerButtonText = computed(() => {
  switch (props.robotState.status) {
    case 'running':
      return 'Stop';
    case 'idle':
      return 'Start';
    case 'error':
      return 'Error';
    default:
      return 'Offline';
  }
});

const powerButtonClass = computed(() => {
  switch (props.robotState.status) {
    case 'running':
      return 'bg-red-800 hover:bg-red-700';
    case 'idle':
      return 'bg-gray-300 hover:bg-gray-200';
    case 'error':
      return 'bg-red-800 hover:bg-red-700';
    default:
      return 'bg-gray-500 hover:bg-gray-400';
  }
});

const canReset = computed(() => {
  return ['idle', 'error'].includes(props.robotState.status);
});

const handlePowerToggle = () => {
  emit('toggle-power');
};

const handleReset = () => {
  emit('reset-robot');
};

const handleFanModeChange = (mode: string) => {
  emit('set-fan-mode', mode, mode === 'static' ? staticFanSpeed.value : undefined);
};

const handleStaticFanSpeedChange = () => {
  emit('set-fan-mode', 'static', staticFanSpeed.value);
};
</script>

<style scoped>
.custom-radio {
  -webkit-appearance: none;
  -moz-appearance: none;
  appearance: none;
  width: 20px;
  height: 20px;
  border-radius: 50%;
  border: 2px solid #000;
  background-color: transparent;
  transition: background-color 0.2s, border-color 0.2s;
}

.custom-radio:checked {
  background-color: #000;
  border-color: #000;
}

@media screen and (-webkit-min-device-pixel-ratio: 0) {
  input[type='range'] {
    overflow: hidden;
    -webkit-appearance: none;
    background-color: #161A1D;
  }

  input[type='range']::-webkit-slider-thumb {
    width: 10px;
    -webkit-appearance: none;
    height: 20px;
    cursor: ew-resize;
    background: #D3D3D3;
    box-shadow: #B1A7A6;
  }
}
</style>