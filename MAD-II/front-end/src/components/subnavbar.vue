<template>
    <div v-if="Role === 'Admin'" >
        <div class="container-fluid ">
            <div class="collapse navbar-collapse justify-content-between" id="navbarCollapse">
                <div class="navbar-nav">
                <router-link to="/aRoleapproval" class="nav-item nav-link">Grant Role</router-link>
                <router-link to="/aCreateRequest" class="nav-item nav-link"> Create Requests </router-link>
                <router-link to="/aEditRequests" class="nav-item nav-link">Edit Requests</router-link>
                <router-link to="/adeleteRequests" class="nav-item nav-link">Delete Requests</router-link>
                </div>
            </div>
        </div>
    </div>

</template>
<script>
    
    export default{
        props: {
            Role: {
            type: String,
            required: true,
            }
        },
}
</script>