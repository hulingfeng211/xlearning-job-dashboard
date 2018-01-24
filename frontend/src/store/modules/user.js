import Cookies from 'js-cookie';
import * as types from '../types' 

const user = {
    state: {
        token:null
    },
    mutations: {
        logout (state, vm) {
            Cookies.remove('user');
            localStorage.clear();
        },
        [types.LOGIN]: (state, data) => {
            localStorage.token = data;
            state.token = data;
        },
        [types.LOGOUT]: (state) => {
            localStorage.removeItem('token');
            state.token = null
        },
        [types.TITLE]: (state, data) => {
            state.title = data;
        }
    }
};

export default user;
