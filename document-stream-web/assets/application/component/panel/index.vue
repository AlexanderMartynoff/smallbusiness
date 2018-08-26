<template>
        <div class="panel">
            <spinner :loading="loading"></spinner>

            <div class="panel-topbar">
                <slot name="topbar"></slot>
            </div>
            
            <div class="panel-content">
                <slot name="content"></slot>
            </div>
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
