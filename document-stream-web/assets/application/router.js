import VueRouter from 'vue-router';

import DocumentMaster from '@application/component/document/master';
import DocumentDetail from '@application/component/document/detail';
import AccountDetail from '@application/component/account/detail';
import ActDetail from '@application/component/act/detail';


export default new VueRouter({
    routes: [
        {path: "/", component: DocumentMaster},
        {path: "/documents", component: DocumentMaster},
        {path: "/document/:id", component: DocumentDetail},

        {path: "/account/:id", component: AccountDetail, rops: true},
        {path: "/account", component: AccountDetail},

        {path: "/act", component: ActDetail}
    ]
});