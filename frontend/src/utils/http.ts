import axios from "axios"

const http = axios.create({
    baseURL: import.meta.env.QVQA_ORIGINS,
    timeout: 3000
})

/// 请求拦截
http.interceptors.request.use(
  config => {
    return config;
  },
  error => {
    // 对请求错误做些什么
    console.error('Aaxios请求出错：', error);
    Promise.reject(error);
  }
)

//响应拦截：后端返回来的结果
http.interceptors.response.use(
    response => {
    /**
     * 对响应数据做点什么
     * 例如，状态码判断
     */
    const res = response.data;
    console.log('Axios响应内容',res)

    return res;
  },
  error => {
    console.error('Axios响应出错：', error);
    return Promise.reject(error);
  }
)

export default http