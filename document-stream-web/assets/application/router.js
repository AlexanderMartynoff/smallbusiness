import VueRouter from 'vue-router'

import AccountDetail from '@/application/component/account/detail'
import AccountMaster from '@/application/component/account/master'
import BankMaster from '@/application/component/bank/master'
import BankDetail from '@/application/component/bank/detail'
import PartnerMaster from '@/application/component/partner/master'
import PartnerDetail from '@/application/component/partner/detail'


export default new VueRouter({
    routes: [
        {path: "/", component: AccountMaster},

        {path: "/account/:id", component: AccountDetail, props: true},
        {path: "/account", component: AccountMaster},

        {path: "/bank", component: BankMaster},
        {path: "/bank/:id", component: BankDetail, props: true},

        {path: "/partners", component: PartnerMaster},
        {path: "/partner", component: PartnerDetail},
        {path: "/partner/:id", component: PartnerDetail, props: true},
    ]
});
