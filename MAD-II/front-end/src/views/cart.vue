<template>
<div>
    <navbar :Role = 'Role'/>   
    <br>
    

    
    <div v-if="m" class="text-center mt-5" >
       <h2>{{  m }}</h2> 
    </div> 

    <div v-else>
        <div class="col-12 text-center mt-3">
            <h2>Your Shopping Cart</h2>
        </div><br><br>
        <div class="product-container">
                <div v-for= "cart in display" :key="cart.cart_id" >
                    <div class="d-flex align-items-start bg-light mb-3" style="height: 100px;">
                        
                        <div class="col" id="font"><img :src=" '/img/' + cart.image_name" class="rounded float-left" alt="image_filename" style="width:140px; height:140px;"></div>
                        <div class="col" id="font">Product ID : {{cart.product_id}} </div>
                        <div class="col" id="font">Name : {{cart.name}} </div>
                        <form  @submit.prevent="updateCartQuantity(cart.cart_id, cart.product_id, cart.quantity)">                       
                            <div class="col" id="font">Quantity : <input v-model="cart.quantity" type="number" min="1" class="form-control" required> </div>
                            <button type="submit" class="btn btn-outline-secondary">change quantity</button>
                        </form>
                        <div class="col" id="font">Price : {{cart.price}} </div>
                        
                        <form @submit.prevent="confirmDeleteCart(cart.cart_id)">
                            <button type="submit" class="btn btn-outline-danger">Remove Item</button>
                        </form>
                    </div>  
                    <br>
                </div>

                <div class="col" id="font">Total : {{ total }}</div><br>
                    <form @submit.prevent="orderDetails">
                        <!-- <input type="hidden" name="total" :value="total"> -->
                        <button type="submit" class="btn btn-outline-success" style="width: 200px; padding: 10px;">Buy All</button>
                    </form>
        </div>
    </div>
        <notification :show="showMessage" :message="message" />
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
        display: [], // Assuming you have this data property
        token: localStorage.getItem('auth_token'),
        Role: localStorage.getItem('role'),
        message: "",
        showMessage: false,
        m: "",
        };
    },
    computed:{
        total (){   
            return this.display.reduce ((total, display) => total + display.price, 0)
        }
    },
    methods: {
        viewProduct(productId) {
        // Implement the viewProduct method
        },
        updateCartQuantity(cartId, productId, quantity) {
        // Implement the updateCartQuantity method
        fetch('http://127.0.0.1:5000/edit',{
        method: 'post',
        headers:{
            'Content-type': 'application/json',
            'Authorization': this.token,
        },
        body: JSON.stringify({ productId: productId, cId: cartId, q: quantity })
        }).then(response => { return response.json()})
        .then(data => {this.message = data, window.location.reload();})
        .catch (Error => {console.log ("Error :" , Error)})
        },
        confirmDeleteCart(cartId) {
            const isConfirm = window.confirm('Are you sure you want to remove product from cart?')
            //window.alert("alert") this shows a dialogbox with a message with ok button.
            if (isConfirm){
                // Implement the confirmDeleteCart method
                fetch('http://127.0.0.1:5000/edit',{
                method: 'delete',
                headers:{
                    'Content-type': 'application/json',
                    'Authorization': this.token,
                },
                body: JSON.stringify({ cId: cartId })
                }).then(response => { return response.json()})
                .then(data => {this.message = data, window.location.reload();})
                .catch (Error => {console.log ("Error :" , Error)})

                // this.showMessage = true;
                // this.message = "Product is removed from cart!";

                // // Hide the notification after a delay (adjust as needed)
                // setTimeout(() => {
                //     this.showNotification = false;
                // }, 2000);


                }
        },
        orderDetails() {
        // Implement the orderDetails method
        this.$router.push({ path: 'deliveryDetails' });
        },
        },
      
    
    mounted(){
        console.log(this.token)
        fetch('http://127.0.0.1:5000/buy',{
        method: 'GET',
        headers:{
            'Content-type': 'aplication/json',
            'Authorization': this.token,
        }
        }).then(response => { return response.json()})
        .then(data => {
        if (data) {
          
          this.display = data;
        } else {
            // No products in the cart, set the message
            this.m = "Cart Is Empty"; // Set the message from the response
        }})
        .catch (Error => {console.log ("Error :" , Error)})
    }
    };
</script>

<style>
    #font {
      font-size :x-large;
      font-style:oblique;
      font-variant: small-caps;
      color: #163d64;
    }

  </style>