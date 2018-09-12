<template>
<div class="application-body">
        <div class="application-sidebar bg-light border-right">
            <h4 class="application-sidebar-header">OPERATIONS</h4>

            <ul class="nav flex-column">
                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent.stop="savePartner(id)">
                        <i class="fas fa-file"></i> Save
                    </a>
                </li>

                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent.stop="openDeleteAlert()" v-if="id">
                        <i class="fas fa-trash"></i> Delete
                    </a>
                </li>
            </ul>
        </div>

        <div class="application-content pl-3 pt-3 pr-3">

            <b-modal v-model="deleting"
                :hide-header="true"
                :no-fade="true"
                @ok="deletePartner(id)"
                @cancel="closeDeleteAlert()">
                <h4>Delete partner?</h4>
            </b-modal>

            <application-toolbar>
                <h1>#{{partner.id || 'NEW'}}</h1>
            </application-toolbar>

            <form>
                <div class="form-row">
                    <div class="form-group col-md-6">
                        <label>Name</label>
                        <input class="form-control" v-model="partner.name" :readonly="readonly" type="text"/>
                    </div>

                    <div class="form-group col-md-3">
                        <label>Bank checking account</label>
                        <input class="form-control" v-model="partner.bankCheckingAccount" :readonly="readonly" type="text"/>
                    </div>

                    <div class="form-group col-md-3">
                        <label>Bank</label>
                        <select class="form-control" name="provider_id" v-model="partner.bankId" :disabled="readonly">
                            <option :value="bank.id" v-for="bank in banks">{{bank.name}}</option>
                        </select>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group col-md-6">
                        <label>Reason code</label>
                        <input class="form-control" v-model="partner.reasonCode" :readonly="readonly" type="text"/>
                    </div>

                    <div class="form-group col-md-3">
                        <label>Address</label>
                        <input class="form-control" v-model="partner.address" :readonly="readonly" type="text"/>
                    </div>

                    <div class="form-group col-md-3">
                        <label>Taxpayer number</label>
                        <input class="form-control" v-model="partner.taxpayerNumber" :readonly="readonly" type="text"/>
                    </div>
                </div>
            </form>

        </div>
    </div>
</template>


<script type="text/javascript">
    import _ from 'lodash'
    import Vue from 'vue'


    export default {
        props: ['id'],

        data() {
            return {
                deleting: false,
                readonly: false,
                banks: [],
                partner: {
                    id: null,
                    name: null,
                    address: null,
                    bankCheckingAccount: null,
                    reasonCode: null,
                    taxpayerNumber: null,
                    bankId: null,
                }
            }
        },

        methods: {
            savePartner(id) {
                if (id) {
                    this.$axios.put(`/api/partner/${id}`, this.partner).then(() => {
                        this.loadPartner(this.id)
                    })
                } else {
                    this.$axios.post('/api/partner', this.partner)
                        .then(partner => {
                            this.$router.push('/partner/' + _.chain(partner).values().head().value())
                        })
                }
            },

            loadPartner(id) {
                return this.$axios.get(`/api/partner/${id}`).then(partner => {
                    this.partner = partner
                })
            },

            deletePartner(id) {
                return this.$axios.delete(`/api/partner/${id}`).then(partner => {
                    this.$router.push('/partners')
                })
            },

            loadBanks() {
                return this.$axios.get('/api/bank').then(banks => {
                    this.banks = banks
                })
            },

            openDeleteAlert() {
                this.deleting = true
            },

            closeDeleteAlert() {
                this.deleting = false
            }
        },

        mounted() {
            this.loadBanks()
            
            if (!_.isEmpty(this.id)) {
                this.loadPartner(this.id)
            }

        }
    }
</script>
