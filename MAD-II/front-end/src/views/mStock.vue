<template>
  <div class="bg" >
      <navbar :Role = 'Role'/>
      <div v-if="m" class="col-12 text-center mt-5">
          <h2> {{ m }} </h2>
      </div>
      <div v-else>
          <section style="background-color: #eee;">
              <br><h3>Out of Stock Products.</h3>
            <div class="text-center container">
              <div class="row">
                <div class="col-md-3"  v-for="product in products" :key="product.id"><br><br>
                  <div class="card" style="background-color: #eef;">
                    <div class="bg-image hover-zoom ripple ripple-surface ripple-surface-light" data-mdb-ripple-color="light">
                      <img :src="'/img/' + product.image_name" class="img-responsive" style="width:100%" alt="Image">
                      <div class="hover-overlay">
                        <div class="mask" style="background-color: rgba(251, 251, 251, 0.15);"></div>
                      </div>
                    </div>
                    <div class="card-body">
                      <h5 class="card-title mb-3"> {{ product.name }}</h5>
                      <p class="text-reset">{{ product.unit }}</p>
                      <p>Price: {{ product.price }} RS.</p>
                      <form @submit.prevent="updateQuantity(product.product_id, product.quantity)" >
                          <input type="number" class="form-control" min="1" v-model="product.quantity" required><br>
                          <button type="submit" class="btn btn-outline-success">Update Quantity</button>&nbsp;
                          <button type="submit" class="btn btn-outline-primary" @click="viewProduct(product.product_id)">View Product</button>
                      </form><br>
                      <notification :show="showMessage" :message="message" />
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
import notification from '@/components/notification.vue'

export default {
components: {
  navbar,
  notification
},
data(){
  return {
      Role: localStorage.getItem('role'),
      token: localStorage.getItem('auth_token'),
      products: [],
      message: "",
      m: null,
  }
},
methods:{
  viewProduct(productd){
    this.$router.push({name: 'mProduct', query:{ id: productd } })
  },
  updateQuantity(productId, quantity){
    const isConfirm = window.confirm("Are You Sure You Want To Update Quantity?")
        if (isConfirm){
            const data = fetch(`http://127.0.0.1:5000/managerWork`,{
            method: 'put',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify({ productId, quantity })
          }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
          })
          .then(data => {
            if (data.message) {
              // this.message = data.message
              // this.showMessage = true
              window.location.reload();
              
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
          // setTimeout(() => {
          //       this.showMessage = false;
          //     }, 200);

  }
}
},
mounted() {
    // Make API request to fetch product list
    fetch('http://127.0.0.1:5000/manager',{
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
          this.m = "No Product is Out of stock!"; // Set the message from the response
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
</style>