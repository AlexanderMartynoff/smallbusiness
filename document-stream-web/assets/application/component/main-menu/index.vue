<template>
    <div class="application-menu bg-primary">

        <div class="application-menu-section-top">
            <b-dropdown class="application-menu-item" variant="link" v-b-tooltip.hover.auto title="Applications" no-caret>
                <template slot="button-content">
                    <i class="fas fa-ellipsis-v"></i>
                </template>
                <b-dropdown-item @click.prevent="$router.push('/account')">
                    Accounts
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/partners')">
                    Partners
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/bank')">
                    Banks
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/task')">
                    Tasks
                </b-dropdown-item>

                <b-dropdown-item @click.prevent="$router.push('/contract')">
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
                <button type="button" class="btn btn-link">
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
    export default {}
</script>
