<template>
    <div class="settting-form">
        <form>
            <div class="form-row">
                <div class="form-group col-md-12">
                    <label>
                        <strong>Recipients</strong>
                    </label>
                    <b-form-checkbox-group v-model="selectedRecipients"
                                           :options="recipients"
                                           stacked>
                    </b-form-checkbox-group>
                </div>

                <div class="form-group col-md-12">
                    <label>
                        <strong>Attachments</strong>
                    </label>
                    <b-form-checkbox-group v-model="selectedAttachments"
                                           :options="attachments"
                                           stacked>
                    </b-form-checkbox-group>
                </div>
            </div>
        </form>
    </div>
</template>

<script type="text/javascript">

    import _ from "lodash"

    export default {
        props: {
            recipients: {type: Array},
            attachments: {type: Array},
            initSubject: {type: String},
            initRecipientsSelection: {type: Array},
            initAttachmentsSelection: {type: Array},
        },

        data() {
            return {
                selectedRecipients: [],
                selectedAttachments: [],
                body: null,
                subject: this.initSubject
            }
        },

        methods: {
            send() {
                return this.$axios.post(`/api/mail`, {
                    recipients: _.map(this.selectedRecipients, recipient => recipient.mail),
                    attachments: this.selectedAttachments,
                    subject: this.subject,
                    body: this.body,
                }).then(response => this.$emit('send'))
            },

            reset() {
                this.selectedRecipients = []
                this.selectedAttachments = []
                this.body = null
            },

            fillSelectedAttachment() {
                
            },
        },

        watch: {
            initRecipientsSelection(recipients) {
                this.selectedRecipients = recipients
            },

            initAttachmentsSelection(attachments) {
                this.selectedAttachments = attachments
            },
        },
    }
</script>
