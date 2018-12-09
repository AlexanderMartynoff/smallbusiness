import Vue from 'vue'
import VueRouter from 'vue-router'
import BootstrapVue from 'bootstrap-vue'

import router from '@/application/router'

import MainMenu from '@/application/component/main-menu/index'
import Checkbox from '@/application/component/checkbox/index'
import Download from '@/application/component/download'
import MailForm from '@/application/component/mail/form'
import MailModal from '@/application/component/mail/modal'
import DatepickerInput from '@/application/component/datepicker/datepicker-input'


import ApplicationContainer from '@/application/component/application/application-container'
import ApplicationContent from '@/application/component/application/application-content'
import ApplicationSidebar from '@/application/component/application/application-sidebar'
import ApplicationBody from '@/application/component/application/application-body'
import ApplicationToolbar from '@/application/component/application/application-toolbar'

import SettingsForm from '@/application/component/settings/form'

import Axios from '@/application/plugin/axios'
import {registry} from '@/application/modifer'


import '@style/layout.scss'
import '@style/style.scss'
import '@style/override.scss'
import '@style/datepicker.scss'

Vue.use(VueRouter)
Vue.use(BootstrapVue)
Vue.use(Axios)

Vue.component('main-menu', MainMenu)
Vue.component('checkbox', Checkbox)
Vue.component('download', Download)
Vue.component('mail-form', MailForm)
Vue.component('mail-modal', MailModal)
Vue.component('datepicker-input', DatepickerInput)

Vue.component('application-container', ApplicationContainer)
Vue.component('application-content', ApplicationContent)
Vue.component('application-sidebar', ApplicationSidebar)
Vue.component('application-body', ApplicationBody)
Vue.component('application-toolbar', ApplicationToolbar)

Vue.component('settings-form', SettingsForm)


const vue = new Vue({
    el: '._root',
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

            error(error) {
                this.axios.counter --
                throw error
            }
        },

        interceptor: {
            request(request) {

                if (_.has(request, 'data')) {
                    registry.modify({
                        url: request.url,
                        method: request.method,
                        direction: 'request',
                    }, request.data)
                }

                return request
            },

            response(response) {
                return registry.modify({
                        url: response.config.url,
                        method: response.config.method,
                        direction: 'response',
                    }, response.data)
            }
        }
    }
})
