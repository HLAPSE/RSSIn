import { createRouter, createWebHistory } from "vue-router";
import Home from "../views/Home.vue";
import Note from "../views/Note.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: Home,
    component: () => import("@/views/Home.vue"),
  },
  {
    path: "/note",
    name: "Note",
    component: Note,
    component: () => import("@/views/Note.vue"),
  },
  {
    path: "/about",
    name: "About",
    component: () => import("@/views/About.vue"),
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

export default router;
