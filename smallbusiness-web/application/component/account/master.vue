<template>
    <div class="application-body">
        <div class="application-sidebar bg-light border-right">
            <h4 class="application-sidebar-header">OPERATIONS</h4>
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/account/new" class="nav-link">
                        <i class="fas fa-plus-circle"></i> Add
                    </router-link>
                </li>
            </ul>
        </div>

        <div class="application-content pl-3 pt-3 pr-3">

            <application-toolbar>
                Accounts
            </application-toolbar>

            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th scope="col">№</th>
                        <th scope="col">Date</th>
                        <th scope="col">Purchaser</th>
                        <th scope="col">Price</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="account in accounts" @click="openAccount(account)">
                        <th scope="row">{{account.id}}</th>
                        <td>{{formatDate(account.date)}}</td>
                        <td>{{account.purchaserName}}</td>
                        <td>{{account.price}}</td>
                    </tr>
                    <tr v-if="accounts.length === 0">
                        <td colspan="4">Records not found</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>


<script type="text/javascript">
    import axios from 'axios'
    import datefns from 'date-fns'

    import {formatTimestamp} from '@/application/instrument'

    const format = 'YYYY/MM/DD'

    export default {
        data: () => {
            return {
               accounts: []
            }
        },

        methods: {
            formatDate(date) {
                return date ? datefns.format(date, format) : null
            },

            loadAccounts: function() {
                this.$axios.get('/api/account').then(accounts => {
                    this.accounts = accounts
                })
            },

            openAccount: function (account) {
                this.$router.push(`/account/${account.id}`)
            }
        },

        mounted: function () {
            this.loadAccounts()
        }
    }
</script>
