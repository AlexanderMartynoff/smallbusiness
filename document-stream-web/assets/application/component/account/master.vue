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
                                <th class="doc">Name</th>
                                <th class="doc">Partner</th>
                                <th class="doc">Date</th>
                            </tr>
                        </thead>
                        <tbody class="doc">
                            <tr class="doc" v-for="account in accounts">
                                <td class="doc">{{account.name}}</td>
                                <td class="doc">{{account.partner_name}}</td>
                                <td class="doc">{{account.date}}</td>
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
        }
    }
</script>
