import { createApp } from 'vue';
import App from './App.vue';
import router from './router';
import { createPinia } from 'pinia';

const pinia = createPinia();

createApp(App)
    .use(pinia)      // primero Pinia
    .use(router)     // luego router
    .mount('#app');
