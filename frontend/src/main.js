import Vue from 'vue';
import iView from 'iview';
import {router} from './router/index';
import store from './store';
import App from './app.vue';
import axios from './http';
import util from './libs/util';
import 'iview/dist/styles/iview.css';

Vue.prototype.axios=axios
Vue.prototype.util=util

Vue.use(iView);

new Vue({
    el: '#app',
    router: router,
    store: store,
    render: h => h(App),
    mounted () {
        this.$store.commit('updateMenulist');
    }
});
