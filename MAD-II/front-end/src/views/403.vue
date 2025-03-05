<template>
    <div class="container mt-5 ">
        <img :src="'/img/neo.gif'" class="img-fluide" style="width:600px; height:450px;" alt="Image">
        <br><p><h2>!!! Access Denied !!!</h2></p>
        <p><h3>If  You Think You Are "The One" Who Can Access This Page.</h3></p>
        <p><h3>Please Contact Admin.</h3></p>
        <button @click="goBack" class="btn btn-outline-secondary">Back  <i class="bi bi-back"></i></button>
    </div>
</template>
<script>
export default{
    methods:{
        goBack(){
            this.$router.go(-2)
        }
    }
}
</script>

