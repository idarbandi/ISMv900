import { createApp } from 'vue'
import App from './App.vue'
import router from './router'
import axios from 'axios';
import VueAxios from 'vue-axios';
import './assets/tailwind.css'
import { Html2CanvasPlugin } from 'vue3-html2canvas';
import './assets/styles/fonts.css'
import { setupApollo } from './apollo'

// Configure axios
axios.defaults.xsrfCookieName = 'csrftoken';
axios.defaults.xsrfHeaderName = "X-CSRFTOKEN";
axios.defaults.baseURL = 'http://localhost:8000';

const app = createApp(App)

app.use(VueAxios, axios)
app.use(router)
app.use(Html2CanvasPlugin);
setupApollo(app)
app.mount('#app')
