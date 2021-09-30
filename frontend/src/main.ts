import { MotionPlugin } from '@vueuse/motion';
import VueViewer from 'v-viewer';
import 'viewerjs/dist/viewer.css';
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
app.use(MotionPlugin);
app.use(VueViewer);
VueViewer.setDefaults({
  zoomRatio: 1,
  title: false,
  navbar: false,
  fullscreen: false,
  tooltip: false,
  toolbar: {
    rotateLeft: true,
    rotateRight: true,
    zoomIn: true,
    zoomOut: true,
    reset: true,
    flipHorizontal: true,
    flipVertical: true
  }
});
app.mount('#app');
