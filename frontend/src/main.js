import { createApp } from 'vue'
import { ElCollapseTransition } from 'element-plus'
import App from './App.vue'

const app = createApp(App).mount('#app')
app.component(ElCollapseTransition.name, ElCollapseTransition)