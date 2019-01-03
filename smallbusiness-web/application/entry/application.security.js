import Vue from 'vue'
import BootstrapVue from 'bootstrap-vue'

import SecurityForm from '@/application/component/security/form'
import Axios from '@/application/plugin/axios'

import '@style/layout.scss'
import '@style/style.scss'
import '@style/override.scss'

Vue.use(BootstrapVue)
Vue.use(Axios)

Vue.component('security-form', SecurityForm)

const _vue = new Vue({
    el: '._vue',
    axios: {
        interceptor: {
            response(response) {
                return response.data
            }
        }
    }
})
