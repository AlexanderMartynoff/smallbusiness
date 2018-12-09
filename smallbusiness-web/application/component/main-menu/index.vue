<template>
    <div class="application-menu bg-primary">
        <b-modal title="System settings"
                 ref="settingsForm"
                 :no-fade="true">
            <settings-form></settings-form>
        </b-modal>

        <div class="application-menu-section-top">
            <b-dropdown class="application-menu-item" variant="link" v-b-tooltip.hover.auto title="Applications" no-caret>
                <template slot="button-content">
                    <i class="fas fa-bars"></i>
                </template>

                <b-dropdown-item @click.prevent="$router.push('/account')" :active="isActive('/account')">
                    Accounts
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/partner')" :active="isActive('/partner')">
                    Partners
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/bank')" :active="isActive('/bank')">
                    Banks
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/task')" :active="isActive('/task')">
                    Tasks
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/contract')" :active="isActive('/contract')">
                    Contracts
                </b-dropdown-item>
            </b-dropdown>

        </div>

        <div class="application-menu-section-bottom">
            <div class="application-menu-item" v-b-tooltip.hover.auto title="Questions?">
                <button type="button" class="btn btn-link">
                    <i class="fas fa-question-circle"></i>
                </button>
            </div>

            <div class="application-menu-item" v-b-tooltip.hover.auto title="Settings">
                <button type="button" class="btn btn-link" @click="showSettingsForm">
                    <i class="fas fa-cog"></i>
                </button>
            </div>

            <div class="application-menu-item" v-b-tooltip.hover.auto title="Logout">
                <button type="button" class="btn btn-link">
                    <i class="fas fa-sign-out-alt"></i>
                </button>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
    import _ from 'lodash'

    export default {

        data() {
            return {
                path: null
            }
        },

        methods: {
            isActive(path) {
                return _.includes(this.$route.path, path)
            },

            showSettingsForm() {
                this.$refs.settingsForm.show()
            }
        }
    }
</script>
