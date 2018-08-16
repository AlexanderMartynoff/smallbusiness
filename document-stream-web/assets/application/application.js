import Vue from 'vue'
import VueRouter from 'vue-router'
import router from '@application/router'
import Spinner from '@application/component/spinner/index';

import '@style/layout.scss'


Vue.use(VueRouter)
Vue.component('spinner', Spinner)

const application = new Vue({router, el: ".vueapp"})
