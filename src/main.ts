import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
// import router from './router'
// import store from './store'
import VueDatePicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'
import VueMultiselect from 'vue-multiselect'
import VueApexCharts from 'vue3-apexcharts';
import ElementPlus from 'element-plus'
import 'element-plus/dist/index.css'



const app = createApp(App)
const pinia = createPinia() // 创建 Pinia 实例
app.use(pinia) // 注册 Pinia
app.use(VueApexCharts);
app.use(ElementPlus)
app.component('VueDatePicker', VueDatePicker)
app.component('VueMultiselect', VueMultiselect)
app.mount('#app')


