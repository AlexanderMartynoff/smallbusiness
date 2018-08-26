<template>
    <div class="modal-frame" v-if="trigger">
        <div class="modal-overlay"></div>

        <div class="card modal-card shadowed" v-if="$slots.header">
            <div class="section modal-card-header">
                <slot name="header"></slot>
            </div>
            <div class="section modal-card-content" v-if="$slots.content">
                <slot name="content"></slot>
            </div>
            <div class="section modal-card-footer" v-if="$slots.footer">
                <slot name="footer"></slot>
            </div>
        </div>
    </div>
</template>


<script type="text/javascript">
    export default {
        props: ['trigger'],

        mounted() {}
    }
</script>
