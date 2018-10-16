<template>
    <component @click="download()" :is="tag">
        <slot></slot>
        <iframe :key="source.key" v-for="source in sources" :src="source.url" :class="classes"></iframe>
    </component>
</template>

<script type="text/javascript">
    import _ from 'lodash'

    function forceArray(arrayMaybe) {
        if (_.isArray(arrayMaybe)) {
            return arrayMaybe
        }
        return []
    }

    export default {
        props: [
            'tag',
            'urls',
            'url',
        ],

        data() {
            return {
                classes: ['d-none'],
                sources: [],
            }
        },

        methods: {
            download() {
                this.sources = _.chain(forceArray(this.urls)).concat(forceArray(this.url)).map((source, index) => ({
                    key: Date.now() + index,
                    url: source
                })).value()
            }
        }
    }
</script>
