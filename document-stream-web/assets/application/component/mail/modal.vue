<template>
    <div class="form-modal">
        <b-modal ref="formModal" title="Send mail" :no-fade="true">
            <div slot="default">
                <mail-form ref="form"
                           :initRecipientsSelection="initRecipientsSelection"
                           :initAttachmentsSelection="initAttachmentsSelection"
                           :subject="subject"
                           :recipients="recipients"
                           :attachments="attachments"
                           @send="onSend()">
                </mail-form>
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
        props: {
            subject: {type: String},
            recipients: {type: Array},
            attachments: {type: Array},
            subject: {type: String},
            initRecipientsSelection: {type: Array},
            initAttachmentsSelection: {type: Array},
        },

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
                this.$refs.form.reset()
                this.$emit('send')
                this.hide()
            },
        }
    }
</script>
