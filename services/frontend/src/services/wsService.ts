import { ref } from 'vue';

export const connectionStatus = ref('connecting');
export const connectionError = ref('');
export const robotState = ref<any>({
    status: 'offline',
    temperature: null,
    power_consumption: null,
    fan_speed: 0,
    fan_mode: 'proportional',
    static_fan_speed: 50,
    uptime: 'N/A',
    logs: [],
});

let ws: WebSocket | null = null;
let reconnectTimeout: number | null = null;

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5487';
const WS_BASE_URL = API_BASE_URL.replace(/^http/, 'ws');

export const connectWebSocket = () => {
    if (ws) {
        ws.close();
    }

    connectionStatus.value = 'connecting';

    try {
        ws = new WebSocket(`${WS_BASE_URL}/ws`);

        ws.onopen = () => {
            connectionStatus.value = 'connected';
            connectionError.value = '';
        };

        ws.onmessage = (event) => {
            try {
                const data = JSON.parse(event.data);
                robotState.value = data;
            } catch (error) {
                console.error('Error parsing WebSocket message:', error);
            }
        };

        ws.onclose = () => {
            connectionStatus.value = 'disconnected';
            scheduleReconnect();
        };

        ws.onerror = (_error) => {
            connectionStatus.value = 'disconnected';
            connectionError.value = 'Connection error';
            scheduleReconnect();
        };
    } catch (error) {
        connectionStatus.value = 'disconnected';
        connectionError.value = 'Failed to create connection';
        scheduleReconnect();
    }
};

const scheduleReconnect = () => {
    if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
    }

    reconnectTimeout = window.setTimeout(() => {
        connectWebSocket();
    }, 3000);
};

export const closeWebSocket = () => {
    if (ws) {
        ws.close();
    }

    if (reconnectTimeout) {
        clearTimeout(reconnectTimeout);
    }
};