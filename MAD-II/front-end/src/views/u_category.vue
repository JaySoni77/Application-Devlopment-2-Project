<template>
<div>
  <navbar :Role = 'Role'/>
  <div v-if="message" class="text-center mt-5">
       <h2>{{  message }}</h2> 
    </div>
    <div v-else>
    <div class="container mt-4">
    <div class="row">
      <div class="col-md-4" v-for="item in list" :key="list.catagory_id">
        <div class="card mb-3">
          <div class="card-body" style="background-color: #eee;">
            <h4 class="card-title">{{ item.name }}</h4><br>
            <p class="card-text">{{ item.description }}</p>
            <button @click="viewProducts(item.catagory_id)" class="btn btn-outline-secondary">View Products</button>
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>
</div>
  </template>

<script>
import navbar from '@/components/u_navbar.vue'
export default {
  components: {
    navbar,
  },
  
      data() {
        return {
          list: [],
          token: localStorage.getItem('auth_token'),
          message: '',
          Role: localStorage.getItem('role'),
        };
      },
      methods:{
        viewProducts(id){
        // Redirect user to /product route with the product ID
        this.$router.push({ name: 'u_product_by_category', query: { id: id } });
      }},
      mounted() {
        // Make API request to fetch product information
        const data = fetch('http://127.0.0.1:5000/api',{
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
            if (data) {
                this.list = data;
        }   else {
            // No products in the cart, set the message
            this.message = "No category is added."; // Set the message from the response
        }})
          .catch(error => {
            console.error('Error:', error);
          });
      }
    }
</script>