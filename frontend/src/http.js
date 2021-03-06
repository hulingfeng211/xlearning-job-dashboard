import axios from 'axios'
import store from './store/index'
import * as types from './store/types'
import {router} from './router/index'

// axios 配置请求操时设置
axios.defaults.timeout = 5000;
//axios.defaults.baseURL = 'https://api.github.com';

// http request 拦截器
axios.interceptors.request.use(
    config => {
        console.log(store.state)
        if (store.state.user.token) {
            config.headers.Authorization = `token ${store.state.user.token}`;
        }
        return config;
    },
    err => {
        return Promise.reject(err);
    });

// http response 拦截器
axios.interceptors.response.use(
    response => {
        console.log(response)
        return response;
    },
    error => {
        if (error.response) {
            switch (error.response.status) {
                case 401:
                    // 401 清除token信息并跳转到登录页面
                    store.commit(types.LOGOUT);
                    router.replace({
                        path: 'login',
                        query: {redirect: router.currentRoute.fullPath}
                    })
            }
        }
        // console.log(JSON.stringify(error));//console : Error: Request failed with status code 402
        return Promise.reject(error.response.data)
    });

export default axios;