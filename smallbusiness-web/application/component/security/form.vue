<template>
    <div class="form-security-container">

        <b-progress class="form-security-progress" v-if="loading" :value="100" variant="primary" animated></b-progress>

        <form class="form-security p-3 shadow-lg rounded border" v-if="!loading" @keypress="onKeypress">
            <div class="form-group">
                <label for="login">Login</label>
                <b-form-input type="text" v-model="login" :state="valid" ref="login" placeholder="Enter login"/>
            </div>
            <div class="form-group">
                <label for="password">Password</label>
                <b-form-input type="password" v-model="password" :state="valid" placeholder="Enter password"/>
            </div>
            <div class="row">
                <div class="col-4">
                    <b-button :variant="variant" @click.stop.prevent="submit">Submit</b-button>
                </div>
                <div class="col-8 d-flex align-items-center justify-content-end">
                    <small v-if="valid === false" class="text-danger">Error diring authentication</small>
                </div>
            </div>
            
        </form>
        <div class="text-right pt-10" v-if="!loading">

            <b-dropdown variant="link"
                        size="sm"
                        :right="true"
                        toggle-class="pr-0"
                        menu-class="shadow-lg">
                <template slot="button-content">
                  <i class="fas fa-cogs"></i>
                </template>
                <b-dropdown-item href="#"
                                 @click.prevent="applyMigrations">
                             <i class="fas fa-database mr-1 align-baseline"></i> Apply migrations</b-dropdown-item>
            </b-dropdown>
        </div>

    </div>

</template>

<script type="text/javascript">

    export default {
        data() {
            return {
                loading: false,
                valid: null,
                login: null,
                password: null,
            }
        },

        methods: {
            submit() {
                this.loading = true

                this.$axios.get('/api/security/authenticate', {
                    params: {
                        login: this.login,
                        password: this.password,
                    }
                }).then(user => {
                    location.replace('/')
                }).catch(error => {
                    this.valid = false
                    this.loading = false
                })
            },

            onKeypress(event) {
                if (event.code === 'Enter') {
                    this.submit()
                }
            },

            applyMigrations() {
                this.loading = true
                this.$axios.post('/api/migration').then(() => {
                    this.loading = false
                })
            },
        },

        computed: {
            variant() {
                return this.valid === false ? 'danger' : 'primary'
            },

            borderClasess() {
                return this.valid === false ? ['border-danger'] : ['border-primary']
            }
        },

        watch: {
            login() {
                this.valid = null
            },

            password() {
                this.valid = null
            }
        }
    }
</script>
