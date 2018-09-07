<template>
    <i :class="[checked ? 'fa-check-square' : 'fa-square']"
       @click="$emit('change', !checked)"
       class="text-primary checkbox far pointer"></i>
</template>

<script type="text/javascript">
    export default {
        model: {
            prop: 'checked',
            event: 'change'
        },

        props: {
            checked: Boolean
        }
    }
</script>
