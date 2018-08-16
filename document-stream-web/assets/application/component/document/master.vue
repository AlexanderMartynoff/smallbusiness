<template>
    <div class="application-body application-body-with-sidebar">
        <div class="application-sidebar">
            <nav>
                <span class="doc block">Documents kind</span>
                <a href="#" class="sublink-1 doc">Act</a>
                <router-link to="/accounts" class="sublink-1 doc">Account</router-link>
                <a href="#" class="sublink-1 doc">Invoice</a>

                <span class="doc block">Shorthand</span>
                <router-link to="/act" class="sublink-1 doc">New Act</router-link>
                <router-link to="/account" class="sublink-1 doc">New Account</router-link>
                <a href="#" class="sublink-1 doc">New Invoice</a>
                <a href="#" class="sublink-1 doc">New Packet</a>
                <a href="#" class="doc">Module help</a>
            </nav>
        </div>
        <div class="application-content">

            <div class="frame">
                <div class="frame-topbar">
                    <h1>Union documents history</h1>
                </div>

                <div class="frame-content">
                    <table class="doc striped hoverable">
                        <thead class="doc">
                            <tr class="doc">
                                <th class="doc">Name</th>
                                <th class="doc">Type</th>
                                <th class="doc">Date</th>
                            </tr>
                        </thead>
                        <tbody class="doc">
                            <tr class="doc">
                                <td data-label="Name" class="doc">Chad</td>
                                <td data-label="Surname" class="doc">Wilberts</td>
                                <td data-label="Alias" class="doc">TheSmith</td>

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
    </div>
</template>

<script type="text/javascript">
    import axios from 'axios'

    export default {
        data: () => {
            return {
               accounts: []
            }
        }
    }
</script>
