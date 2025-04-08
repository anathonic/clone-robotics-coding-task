import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:5487';
const headers = {
    'Content-Type': 'application/json'
};

export const eventService = {
    togglePower: async () => {
        try {
            const response = await axios.post(`${API_BASE_URL}/robot/power`, {}, { headers });

            if (response.status !== 200) {
                throw new Error(`Failed to toggle power: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error toggling power:', error);
        }
    },

    resetRobot: async () => {
        try {
            const response = await axios.post(`${API_BASE_URL}/robot/reset`, {}, { headers });

            if (response.status !== 200) {
                throw new Error(`Failed to reset robot: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error resetting robot:', error);
        }
    },

    setFanMode: async (mode: string, staticValue?: number) => {
        try {
            const response = await axios.post(
                `${API_BASE_URL}/robot/fan`,
                { mode, static_value: staticValue },
                { headers }
            );

            if (response.status !== 200) {
                throw new Error(`Failed to set fan mode: ${response.statusText}`);
            }
        } catch (error) {
            console.error('Error setting fan mode:', error);
        }
    },

    fetchInitialState: async (robotState: any) => {
        try {
            const response = await axios.get(`${API_BASE_URL}/robot/state`, { headers });

            if (response.status !== 200) {
                throw new Error(`Failed to fetch robot state: ${response.statusText}`);
            }

            robotState.value = response.data;
        } catch (error) {
            console.error('Error fetching initial state:', error);
        }
    }
};