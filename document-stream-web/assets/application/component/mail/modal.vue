<template>
    <div class="form-modal">
        <b-modal ref="formModal" title="Send mail">
            <div slot="default">
                <mail-form ref="form" :recipients="recipients" :attachments="attachments" @response="onSend()"></mail-form>
            </div>

            <div slot="modal-footer">
                <button type="button" class="btn btn-secondary" @click="hide()">
                    Cancel
                </button>

                <button type="button" class="btn btn-primary" @click="send()">
                    Send
                </button>
            </div>
        </b-modal>
    </div>

</template>

<script type="text/javascript">
    export default {
        props: [
            'recipients',
            'initSelectedRecipients',
            'attachments',
            'initSelectedAttachments',
        ],

        data() {
            return {}
        },

        methods: {
            show() {
                this.$refs.formModal.show()
            },

            hide() {
                this.$refs.formModal.hide()
            },

            send() {
                this.$refs.form.send()
            },

            onSend() {
                this.hide()
            },
        }
    }
</script>
