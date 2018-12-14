<template>
    <div class="setttings-form">

    <b-tabs>
      <b-tab title="Documents and Reports" active>
        <form class="pt-2 pb-2">
            <div class="form-row">
                <div class="form-group col-md-12 mb-0">
                    <label>Account documents auto-increment</label>
                    <input class="form-control" v-model="configuration.sequence.account" type="text"/>
                </div>
            </div>
        </form>
      </b-tab>

      <b-tab title="About">
        <div class="pt-2 pb-2">
            Lorem ipsum dolor sit amet, consectetur adipiscing elit,
            sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.
            Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
            Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur.
            Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </div>
      </b-tab>

    </b-tabs>
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
                }
            }
        },

        methods: {
            saveConfiguration() {
                this.$axios.put('/api/configuration', this.configuration)
            },

            loadConfiguration() {
                return this.$axios.get('/api/configuration').then(configuration => {
                    this.configuration = configuration
                })
            }
        }
    }
</script>
