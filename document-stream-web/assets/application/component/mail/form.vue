<template>
    <div class="mail-form">
        <form>
            <div class="form-row">
                <div class="form-group col-md-12">
                    <label>Recipients</label>
                    <b-form-select multiple
                                   :select-size="3"
                                   :options="recipients"
                                   v-model="selectedRecipients">
                    </b-form-select>
                </div>

                <div class="form-group col-md-12">
                    <label>Attachments</label>
                    <b-form-select multiple
                                   :select-size="3"
                                   :options="attachments"
                                   v-model="selectedAttachments">
                    </b-form-select>
                </div>
            </div>

            <div class="form-row">
                <div class="form-group col-md-12">
                    <label>Message</label>
                    <textarea v-model="body" class="form-control"></textarea>
                </div>
            </div>
        </form>
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
            return {
                selectedRecipients: [],
                selectedAttachments: [],
                body: null,
            }
        },

        methods: {
            send() {
                return this.$axios.post(`/api/mail`, {
                    recipients: _.map(this.selectedRecipients, recipient => recipient.mail),
                    attachments: this.selectedAttachments,
                }).then(response => this.$emit('response'))
            }
        },
    }
</script>
