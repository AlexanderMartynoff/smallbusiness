<template>
    <div class="application-body application-body-with-sidebar">
        <div class="application-sidebar">
            <nav>
                <span class="doc block">Operations</span>
                <router-link to="/account" class="sublink-1 doc">New Account</router-link>
                <a href="#" class="doc">Module help</a>
            </nav>
        </div>
        
        <div class="application-content">

            <div class="frame">
                <div class="frame-topbar">
                    <h1>Account</h1>
                </div>

                <div class="frame-content">
                    <table class="doc striped hoverable">
                        <thead class="doc">
                            <tr class="doc">
                                <th class="doc">ID</th>
                                <th class="doc">Name</th>
                            </tr>
                        </thead>
                        <tbody class="doc">
                            <tr class="doc" v-for="account in accounts" @click="openAccount(account)">
                                <td class="doc">{{account.id}}</td>
                                <td class="doc">{{account.name}}</td>
                            </tr>
                            <tr class="doc" v-if="accounts.length === 0">
                                <td class="doc" colspan="3">Records not found</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    </div>
</template>


<script type="text/javascript">
    import axios from 'axios'

    export default {
        data: () => {
            return {
               accounts: []
            }
        },

        methods: {
            loadAccounts: function() {
                axios.get('/api/account').then(response => {
                    this.accounts = response.data
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
