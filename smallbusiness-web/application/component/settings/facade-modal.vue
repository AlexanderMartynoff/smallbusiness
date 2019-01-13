<template>
    <div class="settings-facade">

        <settings-user-modal ref="userModal"
                             :user-id="selectedUserId"
                             @onuserformhide="onUserFormHide"
                             @onusercreate="onUserCreate"
                             @onuserdelete="onUserDelete"></settings-user-modal>

        <b-modal title="System settings" ref="facadeModal" :no-fade="true" @ok="saveConfiguration">

            <b-tabs>
                <b-tab title="Documents" active>
                    <form class="mt-2 mb-0">
                        <div class="form-row">
                            <div class="form-group col-md-12 mb-0">
                                <label>Account documents auto-increment</label>
                                <input class="form-control" v-model="configuration.sequence.account" type="text"/>
                            </div>
                        </div>
                    </form>
                </b-tab>

                <b-tab title="Users">

                    <table class="table table-striped mt-2 mb-0">
                        <thead class="bg-light">
                            <tr>
                                <th>ID</th>
                                <th>Login</th>
                                <th>Sudo</th>
                                <th></th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="user in users">
                                <td>{{user.id}}</td>
                                <td>{{user.login}}</td>
                                <td>{{user.sudo}}</td>
                                <td class="text-right">
                                    <b-button size="sm" variant="primary" @click="showUserForm(user)">
                                        <i class="fas fa-cog"></i>
                                    </b-button>
                                </td>
                            </tr>
                            <tr>
                                <td></td>
                                <td></td>
                                <td></td>
                                <td class="text-right">
                                    <b-button size="sm" variant="primary" @click="showUserForm">
                                        <i class="fas fa-plus"></i>
                                    </b-button>
                                </td>
                            </tr>
                            <tr v-if="users.length === 0">
                                <td colspan="4">Users not found</td>
                            </tr>
                        </tbody>
                    </table>
                </b-tab>
            </b-tabs>
        </b-modal>
    </div>
</template>

<script type="text/javascript">

    import _ from "lodash"

    export default {
        props: {},

        data() {
            return {
                configuration: {
                    sequence: {
                        account: null
                    }
                },
                selectedUserId: null,
                users: []
            }
        },

        methods: {
            show() {
                this.$refs.facadeModal.show()
            },

            selectUser(userId=null) {
                this.selectedUserId = userId
            },

            showUserForm(user) {
                this.selectUser(user.id)
                this.$refs.userModal.show()
            },

            onUserDeleteMode() {
                this.$refs.facadeModal.hide()
            },

            onUserFormHide() {
                this.$refs.facadeModal.show()
            },

            onUserCreate(user) {
                this.loadUsers().then(() => this.selectUser(user.id))
            },

            onUserDelete() {
                this.loadUsers().then(() => this.selectUser())
            },

            saveConfiguration() {
                this.$axios.put('/api/configuration', this.configuration)
            },

            loadConfiguration() {
                return this.$axios.get('/api/configuration').then(configuration => {
                    this.configuration = configuration
                })
            },

            loadUsers() {
                return this.$axios.get('/api/user').then(users => {
                    this.users = users
                })
            }
        },
        mounted() {
            this.loadConfiguration()
            this.loadUsers()
        }
    }
</script>
