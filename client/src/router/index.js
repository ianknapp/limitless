import { createRouter, createWebHistory } from 'vue-router'
import { requireAuth, requireNoAuth } from '@/services/auth'
import Home from '@/views/Home.vue'

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "login" */ '../views/Login.vue'),
    beforeEnter: requireNoAuth,
  },
  {
    path: '/signup',
    name: 'Signup',
    component: () => import(/* webpackChunkName: "signup" */ '../views/Signup.vue'),
    beforeEnter: requireNoAuth,
  },
  {
    path: '/password/request-reset/',
    name: 'RequestPasswordReset',
    component: () =>
      import(/* webpackChunkName: "requestreset" */ '../views/RequestPasswordReset.vue'),
    beforeEnter: requireNoAuth,
  },
  {
    path: '/password/reset/confirm/:uid/:token',
    name: 'ResetPassword',
    component: () => import(/* webpackChunkName: "confirmreset" */ '../views/ResetPassword.vue'),
    beforeEnter: requireNoAuth,
  },
  {
    path: '/projects',
    beforeEnter: requireAuth,
    children: [
      {
        path: '',
        name: 'Projects',
        component: () => import(/* webpackChunkName: "dashboard" */ '../views/Projects.vue'),
      },
      {
        path: '/project/:id',
        name: 'Project',
        component: () => import(/* webpackChunkName: "project" */ '../views/Project.vue'),
      },
    ],
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import(/* webpackChunkName: "settings" */ '../views/Settings.vue'),
    beforeEnter: requireAuth,
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'PageNotFound',
    component: () => import('../views/PageNotFound.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  linkActiveClass: 'active-link',
  linkExactActiveClass: 'exact-active-link',
})

export default router
