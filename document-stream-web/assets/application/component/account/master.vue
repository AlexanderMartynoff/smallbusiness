<template>
    <div class="application-body application-body-with-sidebar">
        <div class="application-sidebar">
            <nav>
                <div class="input-group vertical">
                    <label class="doc">Search</label>
                    <input class="doc" size="1">
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

            <div class="frame">
                <table class="doc striped hoverable">
                    <thead class="doc">
                        <tr class="doc">
                            <th class="doc">Name</th>
                            <th class="doc">Surname</th>
                            <th class="doc">Alias</th>
                        </tr>
                    </thead>
                    <tbody class="doc">
                        <tr class="doc">
                            <td data-label="Name" class="doc">Chad</td>
                            <td data-label="Surname" class="doc">Wilberts</td>
                            <td data-label="Alias" class="doc">MrOne</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Adam</td>
                            <td data-label="Surname" class="doc">Smith</td>
                            <td data-label="Alias" class="doc">TheSmith</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Sophia</td>
                            <td data-label="Surname" class="doc">Canderson</td>
                            <td data-label="Alias" class="doc">Candee</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Nick</td>
                            <td data-label="Surname" class="doc">Thomson</td>
                            <td data-label="Alias" class="doc">NickThom</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Mark</td>
                            <td data-label="Surname" class="doc">Gerkis</td>
                            <td data-label="Alias" class="doc">Markie</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">John</td>
                            <td data-label="Surname" class="doc">Fergusson</td>
                            <td data-label="Alias" class="doc">Fergujohn</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Sylvia</td>
                            <td data-label="Surname" class="doc">Pouleau</td>
                            <td data-label="Alias" class="doc">Sylver</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Norman</td>
                            <td data-label="Surname" class="doc">Jones</td>
                            <td data-label="Alias" class="doc">NormalJones</td>
                        </tr>
                        <tr class="doc">
                            <td data-label="Name" class="doc">Trevor</td>
                            <td data-label="Surname" class="doc">Heidel</td>
                            <td data-label="Alias" class="doc">Heidi</td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>
    </div>
</template>

<script type="text/javascript">
    import axios from 'axios'

    export default {
        data: () => {
            return {
               accounts: []
            }
        },

        methods: {
            loadDocuments: function() {
                axios.get('/api/account', {}).then(response => {
                    this.accounts = response.data
                })
            }
        },

        mounted: function() {
            this.loadDocuments();
        }
    }
</script>
