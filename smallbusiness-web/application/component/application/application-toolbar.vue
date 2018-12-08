<template>
    <nav class="application-toolbar sticky-top navbar navbar-expand-lg navbar-light bg-light mb-2 border">
        <a class="navbar-brand" href="#" :style="style" @click.prevent>
            <slot></slot>
        </a>
        <div class="collapse navbar-collapse"></div>
    </nav>
</template>

<script type="text/javascript">
    export default {
        data() {
            return {
                style: {
                    'text-transform': 'uppercase'
                }
            }
        }
    }
</script>
