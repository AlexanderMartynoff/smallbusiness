<template>
<div class="application-body">
        <div class="application-sidebar bg-light border-right">
            <h4 class="application-sidebar-header">OPERATIONS</h4>

            <ul class="nav flex-column">
                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent.stop="saveBank()">
                        <i class="fas fa-file"></i> Save
                    </a>
                </li>

                <li class="nav-item" v-if="isExist">
                    <a href="#" class="nav-link" @click.prevent.stop="openDeleteModal()">
                        <i class="fas fa-trash"></i> Delete
                    </a>
                </li>
            </ul>
        </div>

        <div class="application-content pl-3 pt-3 pr-3">


            <b-modal v-model="deleting"
                :hide-header="true"
                :no-fade="true"
                @ok="deleteBank(id)"
                @cancel="closeDeleteAlert()">
                <h4>Delete bank?</h4>
            </b-modal>

            <application-toolbar>
                <h1>#{{bank.id || 'NEW'}}</h1>
            </application-toolbar>

            <form>
                <div class="form-row">
                    <div class="form-group col-md-8">
                        <label>Name</label>
                        <input class="form-control" v-model="bank.name" type="text"/>
                    </div>

                    <div class="form-group col-md-4">
                        <label>Taxpayer number</label>
                        <input class="form-control" v-model="bank.taxpayerNumber" type="text"/>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group col-md-4">
                        <label>Reason code</label>
                        <input class="form-control" v-model="bank.reasonCode" type="text"/>
                    </div>

                    <div class="form-group col-md-4">
                        <label>Identity code</label>
                        <input class="form-control" v-model="bank.identityCode" type="text"/>
                    </div>

                    <div class="form-group col-md-4">
                        <label>Correspondent account</label>
                        <input class="form-control" v-model="bank.correspondentAccount" type="text"/>
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
                banks: [],
                bank: {
                    id: null,
                    name: null,
                    address: null,
                    reasonCode: null,
                    taxpayerNumber: null,
                    identityCode: null,
                    correspondentAccount: null,
                }
            }
        },

        computed: {
            isExist() {
                return !_.chain(this.id).toNumber().isNaN().value()
            },
        },

        methods: {
            saveBank() {
                if (this.isExist) {
                    this.$axios.put(`/api/bank/${this.id}`, this.bank)
                } else {
                    this.$axios.post('/api/bank', this.bank).then(bank => {
                        this.$router.push('/bank/' + bank['id'])
                    })    
                }

            },

            loadBank(id) {
                this.$axios.get(`/api/bank/${id}`).then(bank => {
                    this.bank = bank
                })
            },

            deleteBank(id) {
                this.$axios.delete(`/api/bank/${id}`).then(bank => {
                    this.$router.push('/bank')
                })
            },

            openDeleteModal() {
                this.deleting = true
            },

            closeDeleteAlert() {
                this.deleting = false
            }
        },

        mounted() {
            if (this.isExist) {
                this.loadBank(this.id)
            }
        },
    }
</script>
