import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import axios from 'axios'

// здесь указываем url, куда будем отправлять все запросы
axios.defaults.baseURL = 'http://192.168.0.3:8000/api/v1/'

createApp(App).use(store).use(router, axios).mount('#app')
