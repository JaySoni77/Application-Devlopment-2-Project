<template>
    <div>
    <navbar :Role = 'Role'/>   
    <br>
    <div v-if="m" class="text-center mt-5" >
       <h2>{{  m }}</h2> 
    </div> 
    <div v-else>
        <div class="col-12 text-center mt-3">
            <h2>Order Details</h2>
        </div><br><br>
        <div class="product-container">
                <div v-for= "i in list" :key="i.order_details_id" >
                    <div class="d-flex align-items-start bg-light mb-3" style="height: 100px;">
                        <div class="col" id="font"><img :src=" '/img/' + i.image_name" class="rounded float-left" alt="image_filename" style="width:140px; height:140px;"></div>
                        <div class="col" id="font">Name : {{i.product_name}} </div>
                        <div class="col" id="font">Price : {{i.price}} </div>
                        <div class="col" id="font">Quantity : {{i.quantity}} </div>
                    </div>  
                    <br>
                </div>
            <button @click="goBack" class="btn btn-outline-secondary ad">Back <i class="bi bi-back"></i></button>
        </div>
        <notification :show="showMessage" :message="message" />
    </div>
</div>
</template>

<script>
import notification from '@/components/notification.vue'
import navbar from '@/components/u_navbar.vue'
    export default {
        components:{
            notification,
            navbar,
        },
    data() {
        return {
        list: [], 
        token: localStorage.getItem('auth_token'),
        Role: localStorage.getItem('role'),
        message: "",
        showMessage: false,
        m: "",
        };
    },methods:{
        goBack(){
            this.$router.go(-1)
        }
    },
    mounted() { 
            const id =this.$route.query.id
            const data = fetch(`http://127.0.0.1:5000/req/${id}`,{
            method: 'put',
            headers: {
            'Content-Type': 'application/json',
            'Authorization': this.token, 
            },
            }).then(response => {
                if (!response.ok) {
                throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.message) {
                    this.message = data.message; // Set the message from the response
                } else {
                    this.list = data;
            }
            })
            .catch(error => {
                console.error('Error:', error);
            }); 
    }
  };
</script>