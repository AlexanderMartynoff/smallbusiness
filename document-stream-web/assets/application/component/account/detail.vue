<template>
    <div class="application-body">
        <div class="application-sidebar bg-light border-right">
            <h4 class="application-sidebar-header">OPERATIONS</h4>

            <ul class="nav flex-column">
                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent.stop="saveAccount(id)">
                        <i class="fas fa-file"></i> Save
                    </a>
                </li>

                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent.stop="toggleReadonly()">
                        <span v-if="readonly">
                            <i class="fas fa-lock-open"></i> Unlock
                        </span>
                        <span v-else>
                            <i class="fas fa-lock"></i> Lock
                        </span>
                    </a>
                </li>

                <li class="nav-item" v-if="isExist()">
                    <a href="#" class="nav-link" @click.prevent.stop="openDeleteAlert()">
                        <i class="fas fa-trash"></i> Delete
                    </a>
                </li>

                <li class="nav-item" v-if="isExist()">
                    <a href="#" class="nav-link" @click.prevent.stop="openPrintAlert()">
                        <i class="fas fa-file-signature"></i> Report
                    </a>
                </li>

                <h4 class="application-sidebar-header">PRODUCTS</h4>

                <li class="nav-item">
                    <a href="#" class="nav-link" @click.prevent.stop="addAccountProduct()">
                        <i class="fas fa-plus-circle"></i> Add
                    </a>
                </li>

                <li class="nav-item" v-if="selectedProducts.length > 0">
                    <a href="#" class="nav-link" @click.prevent.stop="openDeleteAccountProductAlert()">
                        <i class="fas fa-trash"></i> Delete
                    </a>
                </li>
            </ul>
        </div>

        <div class="application-content pl-3 pt-3 pr-3 blur-container">

            <mail-modal ref="mailModal"
                        subject="Account reports"
                        :recipients="mailReportRecipients"
                        :initRecipientsSelection="initMailReportRecipients"
                        :initAttachmentsSelection="initMailReportAttachments"
                        :attachments="mailReportAttachments">
            </mail-modal>

            <b-modal v-model="deleting"
                     :hide-header="true"
                     @ok="deleteAccount(id)"
                     @cancel="closeDeleteAlert()">
                <h4>Delete account?</h4>
            </b-modal>

            <b-modal ref="reportPrintingModal" button-size="sm" title="Select reports for action">

                <b-form-group class="mb-0">
                    <b-form-checkbox-group stacked
                                           v-model="selectedReports"
                                           :options="reports"
                                           text-field="label"
                                           value-field="entity">
                    </b-form-checkbox-group>
                </b-form-group>

                <div slot="modal-footer">

                    <button type="button" class="btn btn-secondary" @click="closePrintAlert()">
                        Cancel
                    </button>

                    <button class="btn btn-primary" type="button" :disabled="selectedReportNoOne()" @click="openReports()">
                        View
                    </button>

                    <button type="button" class="btn btn-primary" :disabled="selectedReportExists()" @click="openMailAlert()">
                        Mail
                    </button>

                    <download :urls="selectedReportUrls" :disabled="selectedReportExists()" tag="button" class="btn btn-primary">
                        Dowload
                    </download>
                </div>

            </b-modal>

            <b-modal v-model="deletingAccountProduct"
                     :hide-header="true"
                     @ok="deleteAccountProductFromAlert(id)"
                     @cancel="closeDeleteAccountProductAlert()">
                <h4>Delete account product?</h4>
            </b-modal>

            <application-toolbar>
                Account ({{id}}) from {{providerBank.name}}
            </application-toolbar>

            <form>
                <div class="form-row mb-2">
                    <div class="col-md-12">
                        <div class="card">
                            <div class="card-body">
                                <h5 class="card-title">Provider bank attributes</h5>
                                <dl class="row">
                                    <dt class="col-sm-3">Name</dt>
                                    <dd class="col-sm-9 text-monospace">{{providerBank.name || '-'}}</dd>

                                    <dt class="col-sm-3">Taxpayer number</dt>
                                    <dd class="col-sm-9 text-monospace">{{providerBank.taxpayerNumber || '-'}}</dd>

                                    <dt class="col-sm-3 text-truncate">Reason code</dt>
                                    <dd class="col-sm-9 text-monospace">{{providerBank.reasonCode || '-'}}</dd>

                                    <dt class="col-sm-3 text-truncate">Identity code</dt>
                                    <dd class="col-sm-9 text-monospace">{{providerBank.identityCode || '-'}}</dd>

                                    <dt class="col-sm-3 text-truncate">Correspondent account</dt>
                                    <dd class="col-sm-9 text-monospace">{{providerBank.correspondentAccount || '-'}}
                                    </dd>
                                </dl>
                            </div>
                        </div>
                    </div>

                </div>

                <div class="form-row">
                    <div class="form-group col-md-6">
                        <label>Purchaser</label>
                        <select class="form-control text-monospace" v-model="account.purchaserId" :disabled="readonly">
                            <option :value="partner.id" v-for="partner in partners">{{partner.name}}</option>
                        </select>
                    </div>

                    <div class="form-group col-md-6">
                        <label>Provider</label>
                        <select class="form-control text-monospace" v-model="account.providerId" :disabled="readonly">
                            <option :value="partner.id" v-for="partner in partners">{{partner.name}}</option>
                        </select>
                    </div>
                </div>

                <div class="form-row">
                    <div class="form-group col-md-6">

                        <label>Currency</label>
                        <select class="form-control text-monospace" v-model="account.currencyUnitId"
                                :disabled="readonly">
                            <option :value="currencyUnit.id" v-for="currencyUnit in currencyUnits">
                                {{currencyUnit.name}}
                            </option>
                        </select>
                    </div>

                    <div class="form-group col-md-6">
                        <label>Reason</label>
                        <input class="form-control text-monospace" v-model="account.reason" :readonly="readonly" type="text"/>
                    </div>
                </div>

                <table class="table table-light">
                    <thead>
                        <tr>
                            <th></th>
                            <th>Name</th>
                            <th>Price</th>
                            <th>Value</th>
                            <th>Unit</th>
                            <th>Amount</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="product in visibleProducts" @change="onProductChange(product)">
                            <td class="center-center-cell">
                                <checkbox v-model="product._selected"/>
                            </td>
                            <td>
                                <input class="form-control text-monospace" :readonly="readonly" v-model="product.name" type="text"/>
                            </td>
                            <td>
                                <input class="form-control text-monospace" :readonly="readonly" v-model="product.price" type="text"/>
                            </td>
                            <td>
                                <input class="form-control text-monospace" :readonly="readonly" v-model="product.value" type="text"/>
                            </td>
                            <td>
                                <select class="form-control text-monospace" v-model="product.timeUnitId" :disabled="readonly">
                                    <option :value="timeUnit.id" v-for="timeUnit in timeUnits">{{timeUnit.name}}</option>
                                </select>
                            </td>
                            <td>
                                <div class="form-control text-monospace">
                                    <strong>{{product.price * product.value}}</strong>
                                </div>
                            </td>
                        </tr>
                        <tr v-if="visibleProducts.length === 0">
                            <td colspan="6">Records not found</td>
                        </tr>
                    </tbody>
                </table>

                <div class="form-row">
                    <div class="form-group col-md-6 offset-md-4">

                        <label>Number as words</label>
                        <div class="form-control text-monospace">
                            <strong>{{totalAmountAsWords}}</strong>
                        </div>
                    </div>

                    <div class="form-group col-md-2">
                        <label>Total amount</label>
                        <div class="form-control text-monospace">
                            <strong>{{totalAmount}}</strong>
                        </div>
                    </div>
                </div>

            </form>

        </div>
    </div>
</template>


<script type="text/javascript">
    import _ from 'lodash'


    export default {
        props: ['id'],

        data() {
            return {
                reports: [
                    {label: 'Account', entity: 'account'},
                    {label: 'Act', entity: 'act'},
                    {label: 'Invoice', entity: 'invoice'},
                ],
                reportsViewing: false,
                selectedReports: [],
                totalAmountAsWords: null,
                providerBank: {},
                deleting: false,
                deletingAccountProduct: false,
                readonly: false,
                partners: [],
                currencyUnits: [],
                timeUnits: [],
                account: {
                    id: null,
                    name: null,
                    providerId: null,
                    purchaserId: null,
                    currencyUnitId: null,
                    products: [],
                    reason: Date.now(),
                }
            }
        },

        methods: {

            selectedReportNoOne() {
                return _.size(this.selectedReports) !== 1
            },

            selectedReportExists() {
                return _.size(this.selectedReports) === 0
            },

            computeReportUrl(report, disposition) {
                return `/api/report/${report}/${this.id}?disposition=${disposition}`
            },

            openReports() {
                _.each(this.selectedReports, report => {
                    window.open(this.computeReportUrl(report, 'inline'), '_blank')
                })
            },

            saveAccount(id) {
                if (this.isExist()) {
                    this.$axios.put(`/api/account/${id}`, this.account).then(() => {
                        this.loadAccount(this.id)
                    })
                } else {
                    this.$axios.post(`/api/account`, this.account)
                        .then(account => {
                            this.$router.push('/account/' + account['id'])
                        })
                }
            },

            loadAccount(id) {
                return this.$axios.get(`/api/account/${id}`).then(account => {
                    this.account = account
                })
            },

            loadPartners() {
                return this.$axios.get(`/api/partner`).then(partners => {
                    this.partners = partners
                })
            },

            loadTimeUnit() {
                return this.$axios.get(`/api/time_unit`).then(timeUnits => {
                    this.timeUnits = timeUnits
                })
            },

            loadCurrencyUnit() {
                return this.$axios.get(`/api/currency_unit`).then(currencyUnits => {
                    this.currencyUnits = currencyUnits
                })
            },

            deleteAccount(id) {
                this.$axios.delete(`/api/account/${this.id}`).then(() => this.$router.push(`/account`))
            },

            addAccountProduct() {
                this.account.products.push({
                    id: Date.now(),
                    name: null,
                    timeUnitId: null,
                    value: null,
                    price: null,
                    _crud: 'insert',
                })
            },

            deleteAccountProductFromAlert() {
                this.deleteAccountProduct(this.selectedProducts)
                this.closeDeleteAccountProductAlert()
            },

            deleteAccountProduct(products) {
                _.each(products, product => {
                    this.$delete(product, '_selected')
                    this.$set(product, '_crud', 'delete')
                })
            },

            openDeleteAccountProductAlert() {
                this.deletingAccountProduct = !_.isEmpty(this.selectedProducts)
            },

            closeDeleteAccountProductAlert() {
                this.deletingAccountProduct = false
            },

            toggleReadonly() {
                this.readonly = !this.readonly
            },

            openReportsAlert() {
                this.reportsViewing = true
            },

            openDeleteAlert() {
                this.deleting = true
            },

            closeDeleteAlert() {
                this.deleting = false
            },

            openPrintAlert() {
                this.$refs.reportPrintingModal.show()
            },

            closePrintAlert() {
                this.$refs.reportPrintingModal.hide()
            },

            openMailAlert() {
                this.$refs.mailModal.show()
            },

            closeMailAlert() {
                this.$refs.mailModal.hide()
            },

            onProductChange(product) {
                if (!_.includes(['delete', 'insert'], product._crud)) {
                    this.$set(product, '_crud', 'update')
                }
            },

            isExist() {
                return !_.chain(this.id).toNumber().isNaN().value()
            },

            partnerToRecipient(partner) {
                return {
                    text: `${partner.name} (${partner.mail})`,
                    value: partner,
                }
            },

            reportToAttachment(report) {
                return {
                    text: report.label,
                    value: {
                        type: 'report',
                        arguments: {
                            entity: report.entity,
                            id: this.id,
                        }
                    },
                }
            },
        },

        computed: {

            mailReportRecipients() {
                return _.map(this.partners, partner => this.partnerToRecipient(partner))
            },

            initMailReportRecipients() {
                return _.chain(this.partners)
                    .filter({id: this.account.purchaserId})
                    .map(partner => this.partnerToRecipient(partner).value)
                    .value()
            },

            mailReportAttachments() {
                return _.map(this.reports, report => this.reportToAttachment(report))
            },

            initMailReportAttachments() {
                return _.chain(this.reports)
                    .filter(report => _.includes(this.selectedReports, report.entity))
                    .map(report => this.reportToAttachment(report).value)
                    .value()
            },

            visibleProducts() {
                return _.filter(this.account.products, product => !_.isEqual(product._crud, 'delete'))
            },

            selectedProducts() {
                return _.filter(this.account.products, product => product._selected === true)
            },

            selectedReportUrls() {
                return _.map(this.selectedReports, report => this.computeReportUrl(report, 'attachment'))
            },

            totalAmount() {
                return _.chain(this.account.products).map(product => product.price * product.value).sum().value()
            },
        },

        watch: {
            'account.providerId'(value) {

                if (_.isNumber(value)) {
                    this.$axios.get(`/api/partner/${value}`).then(partner => {
                        this.providerBank = {
                            name: partner.bankName,
                            checkingAccount: partner.bankCheckingAccount,
                            taxpayerNumber: partner.bankTaxpayerNumber,
                            reasonCode: partner.bankReasonCode,
                            identityCode: partner.bankIdentityCode,
                            correspondentAccount: partner.bankCorrespondentAccount,
                        }
                    })
                }
            },

            'totalAmount'(value) {
                return this.$axios.get(`/api/number_to_word`, {
                    params: {
                        number: value
                    }
                }).then(asWords => {
                    this.totalAmountAsWords = asWords
                }).catch(error => {

                })
            }
        },

        mounted() {
            this.loadPartners()
            this.loadTimeUnit()
            this.loadCurrencyUnit()

            if (this.isExist()) {
                this.loadAccount(this.id)
            }
        }
    }
</script>
