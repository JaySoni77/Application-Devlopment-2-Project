<template>
    <div>
      <navbar :Role = 'Role'/>
        <h2> <em>{{ product.name }}</em> </h2><br> <br>
  
        <div class="container mt-5 row" >  
            <div class="col-md-6">      
              <img :src="'/img/' + product.image_name" class="img-fluide" style="width:350px; height:350px;" alt="Image">
            </div> 
            <div class="col-md-6">
                <p> <strong> Product Name : </strong> {{product.name}}  </p>

                <p> <strong> Price : </strong> {{product.price}} </p>

                <p> <strong> Unit : </strong> {{product.unit}} </p>

                <p> <strong> Expiry_date : </strong> {{product.expiry_date}} </p>
                
                <p> <strong> Description  : </strong> {{product.description}} </p>
                
                <p> <strong>  Category : </strong> {{ product.catagory }} </p>

                <div v-if="product.quantity">
                  <form @submit.prevent = "addToCart">
                    <input v-model="quantity" type="number" min="1" name="quantity" id="quantity" required>&nbsp;
                    <button type="submit" class = "btn btn-outline-warning "> Add to Cart</button>&nbsp;
                    <button @click="goBack" class="btn btn-outline-secondary">Back <i class="bi bi-back"></i></button>
                  </form>
                </div>
                <div v-else><button type="submit" class="btn btn-warning" disabled> Out Of Stock </button></div>
            </div>
            <!-- <notification :show="showMessage" :message="message" /> -->

        </div>
    </div><br>
  </template>

<script>
  // import notification from '@/components/notification.vue'
  import navbar from '@/components/u_navbar.vue'

    export default{
      components: {
        // notification,
        navbar,
      },
      data() {
        return {
          product: [],
          token: localStorage.getItem('auth_token'),
          Role: localStorage.getItem('role'),
          quantity:null,
          message: "",
          showMessage: false,
          q: true
        };
      },
      methods:{
        goBack(){
            this.$router.go(-1)
        },
        addToCart(){
          const productId = this.$route.query.id;
          const data = fetch('http://127.0.0.1:5000/buy',{
            method: 'put',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify({ id: productId, q: this.quantity }),
          }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            this.product = data // Assuming the API response has a 'products' property containing the list of products
            console.log(data)
            // this.message = "Product is added into cart"
            // this.showMessage = true
          })
          .catch(error => {
            console.error('Error:', error);
          })
          this.$router.go(-1)
          // setTimeout(() => {
          //   this.showMessage = false;
          // }, 2000);
        },

      },
      mounted() {
        // retriving product id from home page
        const productId = this.$route.query;
        // Make API request to fetch product information
        const data = fetch('http://127.0.0.1:5000/api',{
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify({ id: productId })
          }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            this.product = data // Assuming the API response has a 'products' property containing the list of products
          })
          .catch(error => {
            console.error('Error:', error);
          });
      }
    }
</script>