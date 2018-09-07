<template>
    <div class="application-menu bg-primary">
        <b-dropdown class="application-menu-item" variant="link" no-caret>
            <template slot="button-content">
                <i class="fas fa-bars"></i>
            </template>
            <b-dropdown-item @click.prevent="$router.push('/accounts')">Accounts</b-dropdown-item>
            <b-dropdown-item href="#">Invoices</b-dropdown-item>
            <b-dropdown-item href="#">Act</b-dropdown-item>
            <b-dropdown-item @click.prevent="$router.push('/partners')">Partners</b-dropdown-item>
            <b-dropdown-item href="#">Banks</b-dropdown-item>
            <b-dropdown-item href="#">Packets</b-dropdown-item>
        </b-dropdown>
        <div class="application-menu-item">
            <button type="button" class="btn btn-link">
                <i class="fas fa-user"></i>
            </button>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {}
</script>
