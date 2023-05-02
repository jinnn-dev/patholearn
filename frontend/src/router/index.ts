import { createRouter, createWebHistory } from 'vue-router';
import { AuthService } from '../services/auth.service';
import { TokenService } from '../services/token.service';
import { appState } from '../utils/app.state';
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
    return next({
      path: '/home'
    });
  }

  if (loggedIn && onlyWhenLoggedOut) {
    return next('/');
  }

  next();
});

export default router;
