<template>
    <div class="bg">
        <navbar :Role = 'Role'/>
        <div>
            <h2>All Orders</h2>
        </div><br>
  
        <!-- <form @submit.prevent="searchOrder" class="d-flex justify-content-center">
            <div class="col-md-6">
            <div class="input-group">
                <input v-model="serchKeyword" type="text" class="form-control" placeholder="Search Order by Order id" required>
                <div class="input-group-append">
                <button type="submit" class="btn btn-warning">Search</button>
                </div>
            </div>
            </div>
        </form><br> -->
  
        <div class="product-container">
            <div v-for="i in orders" :key="i.order_id" class="d-flex align-items-start bg-light mb-3" style="height: 100px;">
            <div class="col-2" id="font">Name: {{ i.receiver }} </div>
            <div class="col-2" id="font">Order ID: {{ i.order_id }} </div>
            <div class="col-1" id="font">Total: {{ i.total }} </div>
            <div class="col-3" id="font">Order Date: {{ i.order_date }} </div>&nbsp;&nbsp;&nbsp;
            <div class="col">
                <input v-model="i.status" @change="updateStatus(i.order_id, i.status)" type="text" placeholder="Order Status" class="form-control">&nbsp;
            </div>&nbsp;
            <!-- <router-link :to="{ name: 'viewOrderAdmin', serchKeyword: { order_id: i.order_id } }">
                <button class="btn btn-success">View Order</button>
            </router-link>&nbsp; -->
    
            <button @click="viewProduct(i.order_id)" class="btn btn-outline-secondary">view Order</button>&nbsp;
            <button @click="deleteOrder(i.order_id)" class="btn btn-outline-danger">Delete Order</button>
            </div>
            <notification :show="showMessage" :message="message" />
        </div>
    </div>
  </template>
  
  <script>
  import navbar from "@/components/u_navbar.vue"
  import notification from "@/components/notification.vue"
  export default {
    components:{
        navbar,
        notification,
    },
    data() {
      return {
        orders: [], // Assuming you will pass orders as a prop or fetch it from the API
        serchKeyword: '',
        status: '',
        Role: localStorage.getItem('role'),
        token: localStorage.getItem('auth_token'),
        showMessage: false,
        message: null,
        status: null

      };
    },
    methods: {
      viewProduct(id){
        this.$router.push({name: 'mViewOrder', query: { id }})
      },

      searchOrder() {
        // Handle search logic here
      },
      updateStatus(orderId, status) {
        const data = fetch(`http://127.0.0.1:5000/managerWork`,{
            method: 'post',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify({ orderId, status })
          }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            if (data.message) {
              this.message = data.message
              this.showMessage = true
              // window.location.reload();
              
          }else if (data.ErRor){
            console.log(data.ErRor)
            this.message = "Opps Something Went Wrong";
              this.showMessage = true
          }
           else {
              this.message = "Something Went Wrong";
              this.showMessage = true
          }
          })
          .catch(error => {
            console.error('Error:', error);
          })
          setTimeout(() => {
                this.showMessage = false;
              }, 2000);

      },
      deleteOrder(orderId) {
        const isConfirm = window.confirm("Are You Sure You Want To Delete Order?")
        if (isConfirm){
            const data = fetch(`http://127.0.0.1:5000/managerWork`,{
            method: 'delete',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify({ orderId })
          }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            if (data.message) {
              this.message = data.message
              this.showMessage = true
              window.location.reload();
              
          }else if (data.ErRoR){
            console.log(data.ErRoR)
            this.message = "Opps Something Went Wrong";
              this.showMessage = true
          }
           else {
              this.message = "Something Went Wrong";
              this.showMessage = true
          }
          })
          .catch(error => {
            console.error('Error:', error);
          })
          setTimeout(() => {
                this.showMessage = false;
              }, 7000);        
        }
      },
    },
    mounted() {

    const data = fetch(`http://127.0.0.1:5000/manager`,{
        method: 'post',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': this.token, 
        },
      }).then(response => {
        if (!response.ok) {
          if (response.status === 403){this.$router.push({name:'forbidden'})}
          
          throw new Error('Network response was not ok');
        }
        return response.json();
      })
      .then(data => {
        if (data.message) {
          this.message = "No Product is Out of stock!";
      } else {
          this.orders = data;
      }
      })
      .catch(error => {
        console.error('Error:', error);
      }); 
    }
  };
  </script>
  
<style scoped> 
.bg{
  background-color: #eee;
  }
</style>
  