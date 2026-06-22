import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import { loadFromStorage } from './store/auth'
import { initTheme } from './store/theme'

loadFromStorage()
initTheme()

const app = createApp(App)

app.use(router)

app.mount('#app')
