<template>
  <navbar :Role = 'Role'/>
    <div style="background-color: #eee;">
        <div v-if="message" class="empty-cart-message text-center mt-5" >
            <h2>{{  message }}</h2> 
        </div>
        <div class="text-center container py-5">
          <div class="row">
            <div class="col-md-3"  v-for="p in products" :key="p.id" @click="viewProduct(p.product_id)"><br><br>
              <div class="card" >
                <div><img :src="'/img/' + p.image_name" class="img-responsive" style="width:80%" alt="Image"></div>
                <div class="card-body">
                  <h5 class="card-title mb-3"> {{ p.name }}</h5>
                  <p class="text-reset">{{ p.unit }}</p>
                  <p>Price: {{ p.price }} RS.</p>
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
          products: [], // Array to store the fetched products
          message: "",
          token: localStorage.getItem('auth_token'),
          Role: localStorage.getItem('role'),
        //   id: null,
        }
      },
      methods: {
        viewProduct(productId) {
          // Redirect user to /product route with the product ID
          this.$router.push({ name: 'u_product', query: { id: productId } });
        }
      },
      mounted() {
        // Make API request to fetch product list
        const id = this.$route.query.id;
        fetch(`http://127.0.0.1:5000/edit/${id}`,{
            method: 'get',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token,
            },
            
          }).then(response => {
            return response.json();
          })
          .then(data => {
            if (data) {
                this.products = data;
        }   else {
            // No products in the cart, set the message
            this.message = "This category is empty."; // Set the message from the response
        }})
          .catch(error => {
            console.log('Error:', error);
          });
      }
    }
  </script>
    