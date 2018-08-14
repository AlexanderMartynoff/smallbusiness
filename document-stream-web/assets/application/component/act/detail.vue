<template>
    <div class="application-body application-body-with-sidebar">
        <div class="application-sidebar">
            <nav>
                <div class="input-group vertical">
                    <label class="doc">Search</label>
                    <input size="1" class="doc"/>
                </div>

                <span class="doc block">Documents kind</span>
                <a href="#" class="sublink-1 doc">Act</a>
                <a href="#" class="sublink-1 doc">Account</a>
                <a href="#" class="sublink-1 doc">Invoice</a>

                <span class="doc block">Operations</span>
                <a href="#" class="sublink-1 doc">Save</a>
                <a href="#" class="sublink-1 doc">Delete</a>
                <a href="#" class="sublink-1 doc">Clone</a>
            </nav>
        </div>

        <div class="application-content">
            <div class="frame grid">
                <div class="spinner-overlay">
                    <div class="spinner tertiary"></div>
                </div>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
    export default {}
</script>
