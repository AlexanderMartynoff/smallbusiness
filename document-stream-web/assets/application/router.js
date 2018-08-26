import VueRouter from 'vue-router';

import AccountDetail from '@application/component/account/detail';
import AccountMaster from '@application/component/account/master';
import ActDetail from '@application/component/act/detail';


export default new VueRouter({
    routes: [
        {path: "/", component: AccountMaster},

        {path: "/account/:id", component: AccountDetail, props: true},
        {path: "/account", component: AccountDetail},
        {path: "/accounts", component: AccountMaster},

        {path: "/act", component: ActDetail}
    ]
});
