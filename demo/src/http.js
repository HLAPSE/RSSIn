import axios from "axios";
import { ElLoading } from "element-plus";
let loading;

const startLoading = () => {
  const options = {
    lock: true,
    text: "loading...",
    background: "rgba(0,0,0,0.7)",
  };
  loading = ElLoading.service(options);
};

const endLoading = () => {
  loading.close();
};

// 请求拦截
axios.interceptors.request.use((config) => {
  startLoading();
  config.headers.Authorization = localStorage.getItem('Token');
  return config;
});
// 响应拦截
axios.interceptors.response.use(
  (response) => {
    endLoading();
    return response;
  },
  (error) => {
    endLoading();
    return Promise.reject(error);
  }
);

export default axios;
