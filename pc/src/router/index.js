import Vue from 'vue'
import Router from 'vue-router'
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

Vue.use(Router)

const createRouter = () =>
  new Router({
    mode: "history",
    routes: [
      {
        path: '/',
        redirect: '/login',
      },
      {
        path: '/login',
        name: 'Login',
        component: () => import("../components/index"),
      }, {
        path: '/home',
        name: 'Home',
        component: () => import("../components/home/index"),
        children: [
          {
            path: '/household/perInfo',
            name: 'User',
            component: () => import("../components/household/perInfo"),
          },
          {
            path: '/admin/user',
            name: 'userManagement',
            component: () => import("../components/administrators/userManagement"),
          },
          {
            path: '/admin/build',
            name: 'buildingManagement',
            component: () => import("../components/administrators/buildingManagement"),
          },
          {
            path: '/admin/house',
            name: 'houseManagement',
            component: () => import("../components/administrators/houseManagement"),
          },
          {
            path: '/household/home',
            name: 'userHome',
            component: () => import("../components/household/home"),
          },
        ]
      }
    ]
  })

const router = createRouter()
router.beforeEach(async (to, from, next) => {
  NProgress.start();
  next();
});

router.afterEach(() => {
  NProgress.done();
});

export default router;
