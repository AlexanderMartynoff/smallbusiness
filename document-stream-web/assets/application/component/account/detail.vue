<template>
<div class="application-body application-body-with-sidebar">
    <div class="application-sidebar">
        <nav>
            <span class="doc block">Operations</span>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="saveAccount(id)">
                <i class="fas fa-file"></i> Save
            </a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="toggleReadonly()">
                <span class="nav-span" v-if="readonly">
                    <i class="fas fa-lock-open"></i> Unlock
                </span>
                <span class="nav-span" v-else>
                    <i class="fas fa-lock"></i> Lock
                </span>
            </a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="openDeleteAlert()" v-if="id">
                <i class="fas fa-trash"></i> Delete
            </a>
            <span class="doc block">Position</span>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="addAccountProduct()">
                <i class="fas fa-plus-circle"></i> Add
            </a>
        </nav>
    </div>

    <div class="application-content">
        <alert :trigger="deleting"
               content="Delete account?"
               @confirm="deleteAccount(id)"
               @discard="closeDeleteAlert()"></alert>

        <alert :trigger="deletingAccountProductMarker"
                content="Delete account product?"
                @confirm="deleteAccountProductFromAlert()"
                @discard="closeDeleteAccountProductAlert()"></alert>

        <panel>
            <template slot="topbar">
                <h1>#{{account.id || 'new'}}, 12.12.2018</h1>
            </template>

            <template slot="content">
                <form class="form-plain">
                    <fieldset>
                        <div class="row">
                            <div class="col-sm">
                                <div class="input-group vertical">
                                    <label class="doc">Purchaser</label>
                                    <select class="doc" name="provider_id" v-model="account.purchaserId" :disabled="readonly">
                                        <option class="doc" :value="purchaser.id" v-for="purchaser in purchasers">{{purchaser.name}}</option>
                                    </select>
                                </div>
                            </div>
                            <div class="col-sm">
                                <div class="input-group vertical">
                                    <label class="doc">Provider</label>
                                    <select class="doc" name="provider_id" v-model="account.providerId" :disabled="readonly">
                                        <option class="doc" :value="provider.id" v-for="provider in providers">{{provider.name}}</option>
                                    </select>
                                </div>
                            </div>
                        </div>
                        <div class="row">
                            <div class="col-sm">
                                <div class="input-group vertical">

                                    <label class="doc">Currency</label>

                                    <select class="doc" name="currency_unit_id" v-model="account.currencyUnitId" :disabled="readonly">
                                        <option class="doc" :value="currencyUnit.id" v-for="currencyUnit in currencyUnits">{{currencyUnit.name}}</option>
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

                    <table class="doc form-table" v-if="account.products.length">
                        <thead class="doc">
                            <tr class="doc">
                                <th class="doc">Name</th>
                                <th class="doc">Price</th>
                                <th class="doc">Value</th>
                                <th class="doc">Unit</th>
                                <th class="doc">Amount</th>
                                <th class="doc form-table-action-col"></th>
                            </tr>
                        </thead>
                        <tbody class="doc">
                            <tr class="doc form-table-action-col" v-for="product in account.products">
                                <td class="doc">
                                    <input :readonly="readonly" v-model="product.name" type="text" class="doc"/>
                                </td>
                                <td class="doc">
                                    <input :readonly="readonly" v-model="product.price" type="text" class="doc"/>
                                </td>
                                <td class="doc">
                                    <input :readonly="readonly" v-model="product.value" type="text" class="doc"/>
                                </td>
                                <td class="doc">
                                    <select class="doc" name="productTimeUnit" v-model="product.timeUnitId" :disabled="readonly">
                                        <option class="doc" :value="timeUnit.id" v-for="timeUnit in timeUnits">{{timeUnit.name}}</option>
                                    </select>
                                </td>
                                <td class="doc">
                                    <input :readonly="readonly" v-model="product.amount" type="text" class="doc"/>
                                </td>
                                <td class="doc form-table-action-col">
                                    <i class="fas fa-trash form-table-action-icon" @click="openDeleteAccountProductAlert(product)"></i>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </form>
            </template>            
            
        </panel>

    </div>
</div>
</template>


<script type="text/javascript">
    import _ from 'lodash'


    export default {
        props: ['id'],

        data() {
            return {
                deleting: false,
                deletingAccountProduct: false,
                readonly: true,
                providers: [],
                purchasers: [],
                currencyUnits: [],
                timeUnits: [],
                account: {
                    name: null,
                    providerId: null,
                    currencyUnitId: null,
                    reason: null,
                    partnerId: null,
                    products: []
                }
            }
        },

        methods: {
            saveAccount(id) {
                if (id) {
                    this.$axios.put(`/api/account/${id}`, this.account)
                } else {
                    this.$axios.post(`/api/account`, this.account)
                        .then(account => {
                            this.$router.push(`/account/` + _.chain(account).values().head().value())
                        })
                }
            },

            loadAccount(id) {
                return this.$axios.get(`/api/account/${id}`).then(account => {
                    this.account = account
                })
            },

            loadPartners() {
                return this.$axios.get(`/api/partner`).then(partners => {
                    this.purchasers = this.providers = partners
                })
            },

            loadTimeUnit() {
                return this.$axios.get(`/api/time_unit`).then(timeUnits => {
                    this.timeUnits = timeUnits
                })
            },

            deleteAccount(id) {
                this.$axios.delete(`/api/account/${this.id}`).then(() => this.$router.push(`/accounts`))
            },

            closeDeleteAccountProductAlert() {
                this.deletingAccountProduct = null
            },

            addAccountProduct() {
                this.account.products.push({
                    id: Date.now(),
                    name: null,
                    timeUnitId: null,
                    value: null,
                    price: null,
                    __phantom__: true
                })
            },

            deleteAccountProductFromAlert() {
                this.deleteAccountProduct(this.deletingAccountProduct)
                this.closeDeleteAccountProductAlert()
            },

            deleteAccountProduct(product) {
                this.account.products = _.filter(this.account.products, _product => {
                    return !_.isEqual(_product.id, product.id)
                })
                
            },

            openDeleteAlert() {
                this.deleting = true
            },

            closeDeleteAlert() {
                this.deleting = false
            },

            openDeleteAccountProductAlert(product) {
                this.deletingAccountProduct = product
            },

            toggleReadonly() {
                this.readonly = !this.readonly
            }
        },

        computed: {
            deletingAccountProductMarker() {
                return !_.isEmpty(this.deletingAccountProduct)
            }
        },

        mounted() {
            this.loadPartners()
            this.loadTimeUnit()
            
            if (!_.isEmpty(this.id)) {
                this.loadAccount(this.id)
            }
        }
    }
</script>
