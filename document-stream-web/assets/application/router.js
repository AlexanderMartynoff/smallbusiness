import VueRouter from 'vue-router';

import DocumentMaster from '@application/component/document/master';
import DocumentDetail from '@application/component/document/detail';
import AccountDetail from '@application/component/account/detail';
import AccountMaster from '@application/component/account/master';
import ActDetail from '@application/component/act/detail';


export default new VueRouter({
    routes: [
        {path: "/", component: DocumentMaster},
        {path: "/documents", component: DocumentMaster},
        {path: "/document/:id", component: DocumentDetail},

        {path: "/account/:id", component: AccountDetail, props: true},
        {path: "/account", component: AccountDetail},
        {path: "/accounts", component: AccountMaster},

        {path: "/act", component: ActDetail}
    ]
});
