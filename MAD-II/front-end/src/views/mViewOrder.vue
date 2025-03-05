<template>
    <div>
        <navbar :Role = "Role"/><br>
        <h2>Order Details</h2><br>
        <div v-for= "i in list" :key="i.order_details_id" ><br>
            <div class="d-flex align-items-start bg-light mb-3" style="height: 100px;">
                <div class="col" id="font"><img :src=" '/img/' + i.image_name" class="rounded float-left" alt="image_filename" style="width:140px; height:140px;"></div>
                <div class="col" id="font">Product Name : {{ i.product_name }} </div>
                <div class="col" id="font">Quantity : {{ i.quantity }} </div>
                <div class="col" id="font">Price : {{ i.price }} </div>
            </div>  
        </div>
        <button @click="goBack" class="btn btn-outline-secondary ad">Back <i class="bi bi-back"></i></button>
    </div>
</template>

<script>
import navbar from '@/components/u_navbar.vue'
import notification from '@/components/notification.vue'
export default{
    components:{
        navbar,
        notification
    },
    data(){
        return{
            list: [],
            Role: localStorage.getItem("role"),
            token: localStorage.getItem("auth_token")
        }
    },
    methods:{
        goBack(){
            this.$router.go(-1)
        }
    },
    mounted(){
        const id = this.$route.query.id
        fetch(`http://127.0.0.1:5000/managerWork/${id}`,{
        method: 'get',
        headers:{
            'Content-type': 'application/json',
            'Authorization': this.token,
        }
        }).then(response => {
                if (!response.ok) {
                if (response.status === 403){this.$router.push({name:'forbidden'})}
                throw new Error('Network response was not ok');
                }
                return response.json();
            })
        .then(data => {
        if (data) {
          this.list = data;
          console.log(this.list)
        } else {
            console.log("Something Went Wrong.")
        }})
        .catch (Error => {console.log ("Error :" , Error)})
    }
}
</script>
<style scoped>
.ad {
  font-size: 16px;
  padding: 8px 25px; /* Adjust padding for button size */
}
</style>