export const routes = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/ai',
    component: () => import('../views/Ai.vue')
  },
  {
    path: '/auth/:pathMatch(.*)*',
    name: 'auth',
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/login',
    name: 'Login',
    meta: {
      public: true,
      onlyWhenLoggedOut: true
    },
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    meta: {
      public: true,
      onlyWhenLoggedOut: true
    },
    component: () => import('../views/auth/Register.vue')
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('../views/Home.vue')
  },
  {
    path: '/slides',
    name: 'Slides',
    meta: {
      adminRoute: true
    },
    component: () => import('../views/Slides.vue')
  },
  {
    path: '/slides/:id',
    name: 'SpecificSlide',
    meta: {
      adminRoute: true
    },
    component: () => import('../components/viewer/SlideViewer.vue')
  },
  {
    path: '/course/:id',
    name: 'Course',
    component: () => import('../views/Course.vue')
  },
  {
    path: '/course/:id/admin',
    name: 'CourseAdmin',
    meta: {
      adminRoute: true
    },
    component: () => import('../views/CourseAdmin.vue')
  },
  {
    path: '/group/:id',
    name: 'TaskGroup',
    component: () => import('../views/TaskGroup.vue')
  },
  {
    path: '/group/:id/admin',
    name: 'TaskGroupAdmin',
    meta: {
      adminRoute: true
    },
    component: () => import('../views/TaskGroupAdmin.vue')
  },
  {
    path: '/task/:id',
    name: 'Task',
    component: () => import('../views/Task.vue')
  },
  {
    path: '/task/:id/admin',
    name: 'Task Admin',
    meta: {
      adminRoute: true
    },
    component: () => import('../views/TaskAdmin.vue')
  },
  {
    path: '/users',
    name: 'Users',
    meta: {
      adminRoute: true
    },
    component: () => import('../views/Users.vue')
  },
  {
    path: '/:pathMatch(.*)*',
    redirect: '/home'
  }
];
