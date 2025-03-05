<template>
    <div class="bg" >
        <navbar :Role = 'Role'/>
        <div v-if="m" class="text-center mt-5">
            <h2>{{  m }}</h2> 
        </div>
        <section v-else >
          <div class="text-center container py-5">
            <div class="row">
              <div> <button class="btn btn-outline-secondary" @click="download">Product List <i class="bi bi-download"></i></button></div>
              <div class="col-md-3"  v-for="product in products" :key="product.id" @click="viewProduct(product.product_id)"><br><br>
                <div class="card pr" >
                  <div class="bg-image hover-zoom ripple ripple-surface ripple-surface-light" data-mdb-ripple-color="light">
                    <img :src="'/img/' + product.image_name" class="img-responsive" style="width:100%" alt="Image">
                    <div class="mask">
                      <div class="d-flex justify-content-start align-items-end h-100">
                        <h5><span class="badge bg-primary ms-2">New</span></h5>
                      </div>
                    </div>
                    <!-- <div class="hover-overlay">
                      <div class="mask" style="background-color: rgba(251, 251, 251, 0.15);"></div>
                    </div> -->
                  </div>
                  <div class="card-body">
                    <h5 class="card-title mb-3"> {{ product.name }}</h5>
                    <p class="text-reset">{{ product.unit }}</p>
                    <p>Price: {{ product.price }} RS.</p>
                  </div>
                </div>
              </div>
              <notification :show="showMessage" :message="message" />
            </div>
          </div>
        </section>
  </div>
</template>
<script>
import navbar from '@/components/u_navbar.vue'
import notification from "@/components/notification.vue"

export default {
  components: {
    navbar,
    notification,
  },
  data(){
    return {
        Role: localStorage.getItem('role'),
        token: localStorage.getItem('auth_token'),
        products: [],
        showMessage: false,
        message: "",
        m: "",
    }
  },
  methods:{
    async download(){
      this.message = "Wait For File To Be Ready..."
      this.showMessage = true
      const res = await fetch('http://127.0.0.1:5000/download_csv',{headers: {'Content-Type': 'application/json','Authorization': this.token}})
      const data = await res.json()
      if (res.ok) {
        const taskId = data['task-id']
        const intv = setInterval(async () => {
          const csv_res = await fetch(`http://127.0.0.1:5000/download_csv/${taskId}`)
          if (csv_res.ok) {
            this.showMessage = false
            clearInterval(intv)
            window.location.href = `http://127.0.0.1:5000/download_csv/${taskId}`
          }
        }, 1000)
      }
    },
    viewProduct(productd){
      this.$router.push({name: 'mProduct', query:{ id: productd } })
    }
  },
  mounted() {
      // Make API request to fetch product list
      fetch('http://127.0.0.1:5000/productCRUD',{
          method: 'GET',
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
          if (data) {
            this.products = data;
        } else {
            // No products in the database, set the message
            this.m = "No Product is added"; // Set the message from the response
        }})
        .catch(error => {
          console.log('Error:', error);
        });
    }
}

</script>

<style scoped> 
.bg{
  background-color: #eee;
  }
.pr{
  background-color: #eef;
}
</style>