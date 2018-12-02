<template>
    <div class="application-container">
        <div class="application-loader" v-if="loading">
            <div class="application-loader-overlay"></div>
            <b-progress :value="100" variant="primary" animated class="application-loader-progress"></b-progress>
        </div>

        <slot></slot>
    </div>
</template>


<script type="text/javascript">
    export default {
        computed: {
            loading() {
                return this.$root.axios.counter > 0
            }
        }
    }
</script>
