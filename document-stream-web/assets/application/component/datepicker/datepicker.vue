<template>
    <div class="datepicker input-group" ref="datepickerEl">
        <input ref="datepickerInputEl"
               type="text" :class="inputClasses"
               v-model="date"
               @focus="showDatepickerDropdownEl()"
               @click.stop>

            <b-card class="datepicker-dropdown" ref="datepickerDropdownEl" v-show="datepickerDropdownElVisible" @click.stop>
                <datepicker-calendar v-model="date" @dayclick="onDayClick"></datepicker-calendar>
            </b-card>

        <div class="input-group-append">
            <button class="btn btn-outline-secondary" type="button" @click.stop="doFocus()">
                <i class="far fa-calendar-alt"></i>
            </button>
        </div>
    </div>
</template>

<script type="text/javascript">
    import _ from 'lodash'
    import Popper from 'popper.js'

    import DatePickerCalendar from '@component/datepicker/datepicker-calendar'

    export default {
        components: {
            'datepicker-calendar': DatePickerCalendar,
        },
        props: {
            inputClass: {type: String},
            autoClose: {
                type: Boolean,
                default: true,
            }
        },
        data() {
            return {
                date: null,
                weeks: [
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 2, 3, 4, 5, 6, 7],
                    [1, 2, 3, 4, 5, 6, 7],
                ],
                attachment: "top left",
                targetAttachment: "bottom left",
                datepickerDropdownElVisible: false,
            }
        },
        computed: {
            inputClasses() {
                return _.chain(this.inputClass).split(' ').concat('form-control').value()
            }
        },
        methods: {

            initPopper() {
                this.$popper = new Popper(this.$refs.datepickerEl, this.$refs.datepickerDropdownEl, {
                    placement: 'bottom-start',
                    modifiers: {
                        offset: {
                            enabled: true,
                            offset: '0, 5'
                        },
                    }
                });
            },

            doFocus() {
                this.$refs.datepickerInputEl.focus()
            },

            hideDatepickerDropdownEl() {
                this.datepickerDropdownElVisible = false
            },

            showDatepickerDropdownEl() {
                this.datepickerDropdownElVisible = true

                this.$nextTick(() => {
                    this.$popper.update()                    
                })
            },

            attacheEventToDocument() {
                document.addEventListener('click', this.bodyClickEventListener = () => this.hideDatepickerDropdownEl())
            },
            
            removeEventToDocument() {
                document.removeEventListener('click', this.bodyClickEventListener)
            },

            onDayClick($event) {
                this.date = $event.date

                if (this.autoClose) {
                    this.hideDatepickerDropdownEl()
                }
            }
        },

        mounted() {
            this.initPopper()
            this.attacheEventToDocument()
        },

        destroyed() {
            this.removeEventToDocument()
        }
    }
</script>
