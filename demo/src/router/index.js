import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Note from "../views/Note.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    component: () => import("@/views/Home.vue"),
    meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
        },
  },
  {
    path: "/note",
    name: "Note",
    component: Note,
    component: () => import("@/views/Note.vue"),
    meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
        },
  },
  {
    path: "/about",
    name: "About",
    component: () => import("@/views/About.vue"),
    meta: {
            requireAuth: true,  // 添加该字段，表示进入这个路由是需要登录的
        },
  },
  {
    path: "/login",
    name: "Login",
    component: () => import("@/views/LoginRegister.vue"),
  },
  {
    path: "/:cacheAll(.*)",
    name: "404",
    component: () => import("@/views/404.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

router.beforeEach((to, from, next) => {
    if (to.meta.requireAuth) {  // 判断该路由是否需要登录权限
        if (localStorage.getItem('Token')) {  // 通过vuex state获取当前的token是否存在
            next();
        }
        else {
            next({
                path: '/login',
                query: {redirect: to.fullPath}  // 将跳转的路由path作为参数，登录成功后跳转到该路由
            })
        }
    }
    else {
        next();
    }
})

export default router;
