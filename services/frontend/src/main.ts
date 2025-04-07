import App from './App.vue'
import './css/tailwind.css'
import router from "./router";
import { createApp } from 'vue'

createApp(App).use(router).mount('#app')