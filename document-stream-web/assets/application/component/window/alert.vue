<template>
    <modal :trigger="trigger">
        <template slot="header">
            <h3>Confirm action</h3>
        </template>
        <template slot="content">
            <h4>{{content}}</h4>
        </template>
        <template slot="footer">
            <div class="alert-modal-footer text-right">
                <button class="secondary bordered" @click="discardClick()">No</button>
                <button class="primary bordered" @click="confirmClick()">Yes</button>
            </div>
        </template>
    </modal>
</template>


<script type="text/javascript">
    export default {
        props: [
            'trigger',
            'content'
        ],

        methods: {
            confirmClick() {
                this.$emit('confirm')
            },
            
            discardClick() {
                this.$emit('discard')
            }
        }
    }
</script>
