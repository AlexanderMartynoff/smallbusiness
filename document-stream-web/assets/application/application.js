import Vue from 'vue'
import VueRouter from 'vue-router'

import router from '@/application/router'
import Spinner from '@/application/component/spinner/index';
import Modal from '@/application/component/window/modal';
import Alert from '@/application/component/window/alert';
import Panel from '@/application/component/panel/index';

import Axios from '@/application/plugin/axios';

import '@style/layout.scss'
import '@style/modal.scss'


Vue.use(VueRouter)
Vue.use(Axios)

Vue.component('spinner', Spinner)
Vue.component('modal', Modal)
Vue.component('alert', Alert)
Vue.component('panel', Panel)


const vue = new Vue({
    el: '.vueapp',
    router: router,
    data() {
        return {
            axios: {
                counter: 0
            }
        }
    },
    axios: {
        event: {
            request(event) {
                this.axios.counter ++
            },

            response(event) {
                this.axios.counter --
            },

            error(event) {
                this.axios.counter --
            }
        },

        interceptor: {
            response(response) {
                return response.data
            }
        }
    }
})
