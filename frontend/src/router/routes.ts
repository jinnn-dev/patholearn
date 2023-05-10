import { RouteRecordRaw } from 'vue-router';

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/home'
  },
  {
    path: '/ai',
    meta: {
      public: true
    },
    component: () => import('../views/ai/Ai.vue')
  },
  {
    path: '/ai/datasets',
    meta: {
      public: true
    },
    component: () => import('../views/ai/datasets/Datasets.vue')
  },
  {
    path: '/ai/datasets/:id',
    meta: {
      public: true
    },
    component: () => import('../views/ai/datasets/Dataset.vue'),
    children: [
      {
        path: '',
        name: 'Dataset Console',
        meta: {
          public: true
        },
        component: () => import('../views/ai/tasks/TaskConsole.vue')
      }
    ]
  },
  {
    path: '/ai/projects',
    meta: {
      public: true
    },
    component: () => import('../views/ai/projects/Projects.vue')
  },
  {
    path: '/ai/projects/:id',
    name: 'Project',
    meta: {
      public: true
    },
    component: () => import('../views/ai/projects/Project.vue')
  },
  {
    path: '/ai/tasks/:id',
    name: 'Ai Task',
    meta: {
      public: true
    },
    component: () => import('../views/ai/tasks/Task.vue'),
    children: [
      {
        path: '',
        name: 'Task Console',
        meta: {
          public: true
        },
        component: () => import('../views/ai/tasks/TaskConsole.vue')
      },
      {
        path: 'metrics',
        name: 'Task Metrics',
        meta: {
          public: true
        },
        component: () => import('../views/ai/tasks/TaskMetrics.vue')
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    meta: {
      public: true,
      onlyWhenLoggedOut: true,
      disableNavigation: true
    },
    component: () => import('../views/auth/Login.vue')
  },
  {
    path: '/register',
    name: 'Register',
    meta: {
      public: true,
      onlyWhenLoggedOut: true,
      disableNavigation: true
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
      adminRoute: true,
      disableNavigation: true
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
    meta: {
      disableNavigation: true
    },
    component: () => import('../views/Task.vue')
  },
  {
    path: '/task/:id/admin',
    name: 'Task Admin',
    meta: {
      adminRoute: true,
      disableNavigation: true
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
