<template>
    <div class="application-menu bg-primary">
        <b-dropdown class="application-menu-item" variant="link" no-caret>
            <template slot="button-content">
                <i class="fas fa-bars"></i>
            </template>
            <b-dropdown-item @click.prevent="$router.push('/account')">Accounts</b-dropdown-item>
            <b-dropdown-item @click.prevent="$router.push('/partners')">Partners</b-dropdown-item>
            <b-dropdown-item @click.prevent="$router.push('/bank')">Banks</b-dropdown-item>
        </b-dropdown>
        <div class="application-menu-item">
            <button type="button" class="btn btn-link">
                <i class="fas fa-meh"></i>
            </button>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {}
</script>
