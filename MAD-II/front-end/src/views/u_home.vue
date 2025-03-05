<template>
  <div>
    <navbar :Role = 'Role'/>
    <div v-if="message" class="text-center mt-5">
       <h2>{{  message }}</h2> 
    </div>
    <div v-else>   
      <section style="background-color: #eee;">
        <div class="text-center container py-5">
          
          <div class="row">
            <div class="col-md-3"  v-for="product in products" :key="product.id" @click="viewProduct(product.product_id)"><br><br>
              <div class="card" style="background-color: #eef;">
                <div class="bg-image hover-zoom ripple ripple-surface ripple-surface-light" data-mdb-ripple-color="light">
                  <img :src="'/img/' + product.image_name" class="img-responsive" style="width:100%" alt="Image">
                  <div class="mask">
                    <div class="d-flex justify-content-start align-items-end h-100">
                      <h5><span class="badge bg-primary ms-2">New</span></h5>
                    </div>
                  </div>
                  <div class="hover-overlay">
                    <div class="mask" style="background-color: rgba(251, 251, 251, 0.15);"></div>
                  </div>
                </div>
                <div class="card-body">
                  <h5 class="card-title mb-3"> {{ product.name }}</h5>
                  <p class="text-reset">{{ product.unit }}</p>
                  <p>Price: {{ product.price }} RS.</p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>
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
        token: localStorage.getItem('auth_token'),
        Role: localStorage.getItem('role'),
        // visible: true,
        message: "",
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
      fetch('http://127.0.0.1:5000/api',{
          method: 'GET',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': this.token,
          },
          
        }).then(response => {
          return response.json();
        })
        .then(data => {
          if (data.message) {
            this.message = data.message;
        } else {
            this.products = data; // Set the message from the response
        }})
        .catch(error => {
          console.log('Error:', error);
        });
    }
  }
</script>
  