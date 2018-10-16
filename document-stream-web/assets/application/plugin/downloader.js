import _ from 'lodash'


export default class DwonloaderPlugin {
    static install(Vue, options) {

        Vue.component('downloader', {
            template: '<iframe v-on=""></iframe>',
            methods: {
                
            }
        })

        Vue.prototype.$download = function() {
            console.log(true)
        }
    }
}
