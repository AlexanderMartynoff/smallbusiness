import Vue from 'vue'
import VueRouter from 'vue-router'
import router from '@application/router'

import '@style/layout.scss'


Vue.use(VueRouter)

const application = new Vue({router, el: ".vueapp"})
