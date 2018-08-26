<template>
    <div class="application-body application-body-with-sidebar">
        <div class="application-sidebar">
            <nav>
                <span class="doc block">Operations</span>
                <router-link to="/account" class="sublink-1 doc">
                    <i class="fas fa-plus-circle"></i> Add
                </router-link>
            </nav>
        </div>
        
        <div class="application-content">

            <div class="panel">
                <div class="panel-topbar">
                    <h1>Account</h1>
                </div>

                <div class="panel-content">
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
