<template>
    <div class="application-body">
        <div class="application-sidebar bg-light border-right">
            <h4 class="application-sidebar-header">OPERATIONS</h4>
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/bank/new" class="nav-link">
                        <i class="fas fa-plus-circle"></i> Add
                    </router-link>
                </li>
            </ul>
        </div>

        <div class="application-content pl-3 pt-3 pr-3">
            <application-toolbar>
                <h1>BANKS</h1>
            </application-toolbar>

            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="bank in banks" @click="openBank(bank)">
                        <th scope="row">{{bank.id}}</th>
                        <td>{{bank.name}}</td>
                    </tr>
                    <tr v-if="banks.length === 0">
                        <td colspan="3">Records not found</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </div>
</template>


<script type="text/javascript">
    import axios from 'axios'

    export default {
        data: () => {
            return {
               banks: []
            }
        },

        methods: {
            loadBanks: function() {
                this.$axios.get('/api/bank').then(banks => {
                    this.banks = banks
                })
            },
            openBank(bank) {
                this.$router.push(`/bank/${bank.id}`)
            }
        },

        mounted: function () {
            this.loadBanks()
        },
    }
</script>
