import axios from "axios";
import router from "./router";
import { ElLoading } from 'element-plus';

// 请求拦截
axios.interceptors.request.use((config) => {
  config.headers.Authorization = localStorage.getItem('Token');
  return config;
});
// 响应拦截
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response) {
      let loadingInstance = ElLoading.service();
      loadingInstance.close();
      switch (error.response.status) {
        case 401:
          // 返回 401 清除token信息并跳转到登录页面
          localStorage.clear()
          router.replace({
            path: 'login',
            query: { redirect: router.currentRoute.fullPath }
          });
        case 500:
          localStorage.clear()
              router.replace({
                  path: 'login',
                  query: {redirect: router.currentRoute.fullPath}
              })
      }
    }
    return Promise.reject(error);
  }
);

export default axios;
