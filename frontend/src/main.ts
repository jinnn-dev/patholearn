import { createApp } from 'vue';
import * as icons from '../icons';
import App from './App.vue';
import Icon from './components/Icon.vue';
import './index.css';
import router from './router';
import { ApiService } from './services/api.service';
import { TokenService } from './services/token.service';

Icon.add(Object.values({ ...icons }));

if (TokenService.getToken()) {
  ApiService.setHeader();
  ApiService.mount401Interceptor();
}

const app = createApp(App);
app.use(router);

app.mount('#app');
