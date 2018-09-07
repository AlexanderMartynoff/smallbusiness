<template>
     <div class="application-body">
        <div class="application-sidebar bg-light border-right">
            <h4 class="application-sidebar-header">OPERATIONS</h4>
            <ul class="nav flex-column">
                <li class="nav-item">
                    <router-link to="/partner" class="nav-link">
                        <i class="fas fa-plus-circle"></i> Add
                    </router-link>
                </li>
            </ul>
        </div>

        <div class="application-content pl-3 pt-3 pr-3">

            <nav aria-label="breadcrumb" class="sticky-top">
                <ol class="breadcrumb">
                    <li class="breadcrumb-item"><a href="#">Home</a></li>
                    <li class="breadcrumb-item"><a href="#">Partners</a></li>
                </ol>
            </nav>

            <h1>PARTNERS</h1>

            <table class="table table-striped table-hover">
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="partner in partners" @click="openPartner(partner)">
                        <td scope="row">{{partner.id}}</td>
                        <td>{{partner.name}}</td>
                    </tr>
                    <tr v-if="partners.length === 0">
                        <td colspan="2">Records not found</td>
                    </tr>
                </tbody>
            </table>

        </div>
    </div>
</template>


<script type="text/javascript">
    export default {
        data: () => {
            return {
               partners: []
            }
        },

        methods: {
            loadPartners: function() {
                this.$axios.get('/api/partner').then(partners => {
                    this.partners = partners
                })
            },

            openPartner: function (partner) {
                this.$router.push(`/partner/${partner.id}`)
            }
        },

        mounted: function () {
            this.loadPartners()
        }
    }
</script>
