<template>
    <div class="mail-form">
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

            <div class="form-row">
                <div class="form-group col-md-12">
                    <label>Subject</label>
                    <input v-model="subject" class="form-control"/>
                </div>
                <div class="form-group col-md-12">
                    <label>Message</label>
                    <textarea v-model="body" class="form-control"></textarea>
                </div>
            </div>
        </form>
    </div>
</template>

<script type="text/javascript">
    /**
     * :recipients - List recipeints.
     */

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
