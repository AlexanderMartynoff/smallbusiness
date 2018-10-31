<template>
    <div class="datepicker-calendar">

    <div class="row">
        <div class="col text-left">
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-light">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <button type="button" class="btn btn-light">Junary</button>
                <button type="button" class="btn btn-light">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
        <div class="col text-right">
            <div class="btn-group" role="group">
                <button type="button" class="btn btn-light">
                    <i class="fas fa-chevron-left"></i>
                </button>
                <button type="button" class="btn btn-light">2018</button>
                <button type="button" class="btn btn-light">
                    <i class="fas fa-chevron-right"></i>
                </button>
            </div>
        </div>
    </div>
        <table class="datepicker-calendar-table">
            <thead>
                <th>Mo</th>
                <th>Tu</th>
                <th>We</th>
                <th>Th</th>
                <th>Fr</th>
                <th>Sa</th>
                <th>Su</th>
            </thead>
            <tr v-for="week in weeks">
                <td v-for="day in week">
                    <button type="button" class="btn btn-light btn-block" @click="onDayClick(day)">
                        {{day}}
                    </button>
                </td>
            </tr>
        </table>
    </div>
</template>

<script type="text/javascript">
    import _ from 'lodash'
    import moment from 'moment'


    export default {
        data() {
            return {
                weeks: [
                    [1, 2, 3, 4, 5, 6, 7],
                    [8, 9, 10, 11, 12, 13, 14],
                    [14, 15, 16, 17, 18, 19, 20],
                    [21, 22, 23, 24, 25, 26, 27],
                    [28, 29, 30, 31, 1, 2, 3],
                    [4, 5, 6, 7, 8, 9, 10],
                ]
            }
        },
        
        methods: {
            onDayClick(date) {
                this.$emit('dayclick', {date})
            }
        },
    }
</script>
