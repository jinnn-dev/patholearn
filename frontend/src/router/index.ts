import { createRouter, createWebHistory } from 'vue-router';
import { AuthService } from '../services/auth.service';
import { TokenService } from '../services/token.service';
import { appLoading, appState } from '../utils/app.state';
import { routes } from './routes';
import Session from 'supertokens-web-js/recipe/session';

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach(async (to, _from, next) => {
  const onlyWhenLoggedOut = to.matched.some((record) => record.meta.onlyWhenLoggedOut);
  const adminRoute = to.matched.some((record) => record.meta.adminRoute);
  const loggedIn = await Session.doesSessionExist();

  if (!onlyWhenLoggedOut && !loggedIn) {
    return next({
      path: '/login',
      query: { redirect: to.fullPath }
    });
  }

  if (!onlyWhenLoggedOut && appState.user === null) {
    try {
      const user = await AuthService.getUser();
      appState.user = user;
    } catch (err) {
      AuthService.logout();
    }
  }

  if (adminRoute && !appState.user?.is_superuser) {
    appLoading.value = false;

    return next({
      path: '/home'
    });
  }

  if (loggedIn && onlyWhenLoggedOut) {
    appLoading.value = false;
    return next('/');
  }

  if (to.path === '/login' || to.path === '/register') {
    appLoading.value = true;
  } else {
    appLoading.value = false;
  }

  next();
});

export default router;
