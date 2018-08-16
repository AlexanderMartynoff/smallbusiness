<template>
    <div class="spinner-overlay" v-if="loading">
        <div class="spinner tertiary"></div>
    </div>
</template>

<script type="text/javascript">
    export default {
        props: ['loading']
    }
</script>
