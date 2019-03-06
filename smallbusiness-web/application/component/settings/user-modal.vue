<template>
    <div class="user-modal">

        <b-modal ref="deleteModal"
                 :hide-header="true"
                 :no-fade="true"
                 @show="onDeleteModalShow"
                 @hide="onDeleteModalHide"
                 @cancel="show"
                 @ok.prevent="deleteUser">
            Do you realy wanna delete user <strong>{{name}}</strong>?
        </b-modal>

        <b-modal :title="title"
                 ref="modal"
                 :no-fade="true"
                 @hidden="onUserFormHide">

            <template slot="modal-footer">
                <b-button variant="secondary" @click="onCancel">Cancel</b-button>
                <b-button variant="danger"
                          @click="onDelete"
                          :disabled="user.sudo"
                          v-if="isReal">Delete</b-button>
                <b-button variant="primary" @click="onSave">Save</b-button>
            </template>

            <form class="mt-2 mb-0">
                <div class="form-row">                    
                    <div class="form-group col-md-12">
                        <label>Login</label>
                        <input class="form-control" v-model="user.login" type="text"/>
                    </div>

                    <div class="form-group col-md-12">
                        <label>Password</label>
                        <input class="form-control" v-model="user.password" type="text"/>
                    </div>

                    <div class="form-group col-md-12" v-if="user.permissions.length > 0">
                        <label>
                            Permissions
                        </label>
                        
                        <table class="table table-striped mt-2 mb-0">
                            <thead class="bg-light">
                                <tr>
                                    <td colspan="1"></td>
                                    <td colspan="4">
                                        <b-form-checkbox class="float-right mr-0"
                                                         v-model="user.sudo"
                                                         :unchecked-value="false"
                                                         :value="true">sudo</b-form-checkbox>
                                    </td>
                                </tr>
                                <tr>
                                    <th>Entity</th>
                                    <th>C</th>
                                    <th>R/V</th>
                                    <th>U</th>
                                    <th>D</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="permission in user.permissions">
                                    <td>{{permission.entity}}</td>
                                    <td><checkbox v-model="permission.create"/></td>
                                    <td><checkbox v-model="permission.read"/></td>
                                    <td><checkbox v-model="permission.update"/></td>
                                    <td><checkbox v-model="permission.delete"/></td>
                                </tr>
                            </tbody>
                        </table>
                    </div>

                </div>
            </form>
        </b-modal>
    </div>


</template>

<script type="text/javascript">
    import _ from "lodash"

    export default {
        props: {
            userId: Number,
        },

        data() {
            return {
                user: {
                    permissions: [],
                },
                deleteMode: false,
                sudo: false,
            }
        },

        methods: {
            onDeleteModalShow() {
                this.deleteMode = true
            },

            onDeleteModalHide() {
                this.deleteMode = false
            },
            
            show() {
                this.$refs.modal.show()
            },

            onUserFormHide() {
                if (!this.deleteMode) {
                    this.$emit('onuserformhide')
                }
            },

            activateUser() {
                this.$axios.put(`/api/user/${this.userId}/activate`)
            },

            onCancel() {
                this.$refs.modal.hide()
            },

            deleteUser() {
                this.$axios.delete(`/api/user/${this.userId}`).then(() => {
                    this.onDeleteModalHide()
                    this.onUserFormHide()
                    this.$emit('onuserdelete')
                })
            },

            onDelete() {
                this.$refs.deleteModal.show()
            },

            onSave() {
                this.saveUser()
            },

            saveUser() {
                if (_.isNull(this.userId)) {
                    this.$axios.post(`/api/user`, this.user).then(user => {
                        this.$emit('onusercreate', user)
                    })
                } else {
                    this.$axios.put(`/api/user/${this.userId}`, this.user).then(() => {
                        this.$refs.modal.hide()
                    })
                }
            },

            loadUser(userId) {
                return this.$axios.get(`/api/user/${userId}`).then(user => {
                    if (_.isEmpty(user)) {
                        this.user = {
                            permissions: []
                        }
                    } else {
                        this.user = user
                    }

                    return user
                })
            },
        },

        computed: {
            isReal() {
                return !_.isNull(this.userId)
            },

            isSudo() {
                if (_.isEmpty(this.user)) {
                    return false
                }
                return this.user.sudo
            },

            name() {
                if (!_.isEmpty(this.user) && !_.isEmpty(this.user.login)) {
                    return this.user.login
                }
                return null
            },

            title() {
                if (_.isNull(this.name)) {
                    return 'User'
                }
                return `User (${this.name})`
            }
        },

        watch: {
            userId: {
                immediate: true,
                handler(userId) {
                    if (!_.isNull(userId)) {
                        this.loadUser(userId)                        
                    } else {
                        this.user = {
                            permissions: []
                        }
                    }
                }
            }
        }
    }
</script>
