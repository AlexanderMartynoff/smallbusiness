<template>
<div class="application-body application-body-with-sidebar">
    <div class="application-sidebar">
        <nav>
            <span class="doc block">Operations</span>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="saveAccount(id)">Save</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="toggleReadonly()">
                {{readonly ? 'Edit' : 'Hold' }}
            </a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="deleteAccount(id)">Delete</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Clone</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Add position</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Remove position</a>
        </nav>
    </div>
    <div class="application-content">
        <div class="frame">

            <spinner :loading="loading"></spinner>

            <div class="frame-topbar">
                <h1>{{account.name}} #{{account.id || 'new'}}, 12.12.2018</h1>
            </div>
            <div class="frame-content">
                <form class="form-plain">
                    <fieldset>
                            <div class="row">
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Name</label>
                                        <input v-model="account.name" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Partner</label>
                                        <input v-model="account.partner" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm">
                                    <div class="input-group vertical">

                                        <label class="doc">Currency</label>

                                        <select class="doc" name="currency" v-model="account.currency" :disabled="readonly">
                                            <option class="doc" value="ruble">Ruble</option>
                                            <option class="doc" value="american-dollar">American dollar</option>
                                            <option class="doc" value="euro">Euro</option>
                                        </select>
                                    </div>
                                </div>
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Reason</label>
                                        <input v-model="account.reason" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                            </div>
                    </fieldset>

                        <fieldset>
                            <div class="row">
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <label class="doc">Name</label>
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <label class="doc">Price</label>
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <label class="doc">Value</label>
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <label class="doc">Total</label>
                                    </div>
                                </div>
                            </div>
                            <div class="row" v-for="item in account.items">
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="item.name" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="item.price" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="item.value" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="item.total" :readonly="readonly" type="text" class="doc">
                                    </div>
                                </div>
                            </div>
                    </fieldset>
                </form>
            </div>
        </div>
    </div>
</div>
</template>

<script type="text/javascript">
    import axios from 'axios'
    import _ from 'lodash'

    export default {
        props: ['id'],
        data: function() {
            return {
                readonly: true,
                account: {
                    name: null,
                    partner: null,
                    currency: 'ruble',
                    reason: null,
                    items: [{}]
                },
                loading: false
            }
        },

        methods: {
            saveAccount (id) {
                this.loading = true

                if (id) {
                    axios.put(`/api/account/${id}`, this.account).finally(response => this.loading = false)
                } else {
                    axios.post(`/api/account`, this.account)
                        .then(response => {
                            this.$router.push(`/account/` + _.chain(response.data).values().head().value())
                        }).finally(response => this.loading = false)
                }
            },

            loadAccount(id) {
                this.loading = true

                return axios.get(`/api/account/${id}`).then(response => {
                    this.account = _.defaults(response.data, {items: [{}]})
                }).finally(() => {
                    this.loading = false
                })
            },

            deleteAccount (id) {
                this.loading = true

                axios.delete(`/api/account/${this.id}`).finally(response => {
                    this.loading = false
                }).then(() => this.$router.push(`/accounts`))
            },
            toggleReadonly() {
                this.readonly = !this.readonly
            }
        },

        mounted () {
            if (_.isEmpty(this.id)) {
                this.readonly = false
            } else {
                this.loadAccount(this.id)
            }
        }
    }
</script>
