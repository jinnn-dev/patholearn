import VueViewer from 'v-viewer';
import 'viewerjs/dist/viewer.css';
import { createApp } from 'vue';
import * as icons from '../icons';
import App from './App.vue';
import Icon from './components/general/Icon.vue';
import './index.css';
import router from './router';
import { ApiService } from './services/api.service';
import { TokenService } from './services/token.service';
import * as Sentry from '@sentry/vue';
import { BrowserTracing } from '@sentry/tracing';

import { getEnv } from './config';
import Vue from 'vue';

Icon.add(Object.values({ ...icons }));

if (TokenService.getToken()) {
  ApiService.setHeader();
  ApiService.mount401Interceptor();
}

const app = createApp(App);

app.use(router);
app.use(VueViewer);

Sentry.init({
  app,
  dsn: getEnv('SENTRY_DSN'),
  environment: getEnv('SENTRY_ENVIRONMENT'),
  integrations: [
    new BrowserTracing({
      routingInstrumentation: Sentry.vueRouterInstrumentation(router),
      tracePropagationTargets: ['localhost', 'patholearn.de', /^\//]
    })
  ]
});

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
