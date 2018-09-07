import Vue from 'vue'
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue'

import router from '@/application/router'
import Spinner from '@/application/component/spinner/index';
import Modal from '@/application/component/window/modal';
import Alert from '@/application/component/window/alert';
import Panel from '@/application/component/panel/index';
import MainMenu from '@/application/component/main-menu/index';
import Checkbox from '@/application/component/checkbox/index';

import Axios from '@/application/plugin/axios';

import '@style/layout.scss'
import '@style/style.scss'
import '@style/override.scss'


Vue.use(VueRouter)
Vue.use(BootstrapVue)
Vue.use(Axios)

Vue.component('spinner', Spinner)
Vue.component('modal', Modal)
Vue.component('alert', Alert)
Vue.component('panel', Panel)
Vue.component('panel', Panel)
Vue.component('main-menu', MainMenu)
Vue.component('checkbox', Checkbox)


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
