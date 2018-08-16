<template>
<div class="application-body application-body-with-sidebar">
    <div class="application-sidebar">
        <nav>
            <span class="doc block">Operations</span>
            <a href="#" class="sublink-1 doc" @click.prevent.stop="save()">Save</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Edit</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Delete</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Clone</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Add position</a>
            <a href="#" class="sublink-1 doc" @click.prevent.stop>Remove position</a>

            <span class="doc block">Navigation</span>
            <router-link to="/accounts" class="sublink-1 doc">Back</router-link>
            <a href="#" class="doc" @click.prevent.stop>Module help</a>
        </nav>
    </div>
    <div class="application-content">
        <div class="frame">

            <spinner :loading="loading"></spinner>

            <div class="frame-topbar">
                <h1>Account #Null, Null, 12.12.2018</h1>
            </div>
            <div class="frame-content">
                <form class="form-plain">
                    <fieldset>
                        <div class="container">
                            <div class="row">
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Name</label>
                                        <input v-model="account.name" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Partner</label>
                                        <input v-model="account.partner" type="text" class="doc">
                                    </div>
                                </div>
                            </div>
                            <div class="row">
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Date</label>
                                        <input v-model="account.date" type="date" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm">
                                    <div class="input-group vertical">
                                        <label class="doc">Reason</label>
                                        <input v-model="account.reason" type="text" class="doc">
                                    </div>
                                </div>
                            </div>
                        </div>

                        
                    </fieldset>

                    <fieldset>
                        <div class="container">
                        <div class="row">
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="account.date" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="account.date" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="account.reason" type="text" class="doc">
                                    </div>
                                </div>
                                <div class="col-sm-3">
                                    <div class="input-group vertical">
                                        <input v-model="account.reason" type="text" class="doc">
                                    </div>
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

    export default {
        data: function() {
            return {
                account: {
                    name: null,
                    partner: null,
                    date: null,
                    reason: null
                },
                loading: false
            }
        },

        methods: {
            save: function () {
                this.loading = true

                axios.put('/api/account', this.account).then(response => {
                    this.loading = false
                }).catch(() => {
                    this.loading = false
                })
            }
        }
    }
</script>
