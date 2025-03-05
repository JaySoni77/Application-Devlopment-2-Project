<template>
    <div>
      <navbar :Role = 'Role'/>
        <!-- <h2> <em>{{ product.name }}</em> </h2><br> <br> -->
  
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

                <p> <strong>  Quantity : </strong> {{ product.quantity }} </p>

                <button @click = "editProduct(product.product_id)" class = "btn btn-outline-primary"> Edit Product</button>&nbsp;
                <button @click = "deleteProduct(product.product_id)" class = "btn btn-outline-danger"> Delete Product</button>

            </div>
            <notification :show="showMessage" :message="message" />

        </div>
    </div><br>
</template>

<script>
import navbar from '@/components/u_navbar.vue'
import notification from '@/components/notification.vue'
export default{
    components: {
        notification,
        navbar,
    },
    data() {
        return {
            product: [],
            token: localStorage.getItem('auth_token'),
            Role: localStorage.getItem('role'),
            message: "",
            showMessage: false,
        }
    },
    methods: {
        editProduct(productId){
            this.$router.push({path: '/mEditProduct', query: { productId } })
        },
        deleteProduct(productId){
          const isConfirm = window.confirm("Are Sure You Want To Delete The Product?")
          if (isConfirm){
              console.log(productId)
              fetch(`http://127.0.0.1:5000/productCRUD/${productId}`,{
              method: 'delete',
              headers: {
                  'Content-Type': 'application/json',
                  'Authorization': this.token,
              },
              }).then(response => {
                if (!response.ok) {
                if (response.status === 403){this.$router.push({name:'forbidden'})}
                throw new Error('Network response was not ok');
                }
                return response.json()})
              .then(data => {
                  if (data && data.Message === "Product deleted successfully.") {
                  this.message = data.Message;
                  this.showMessage = true,
                  setTimeout(() => {
                    this.showMessage = false;
                    this.$router.go(-1)
                }, 2000);
              } else if (data.Error ){
                  this.message = data.Error,
                  this.showMessage = true,
                  setTimeout(() => {this.showMessage = false}, 4000);
              }
              else if (!data) {
                  this.message = "Something went wrong!";
              }})
              .catch(error => {
                  console.log('Error:', error)});

          }
          
    }},
    mounted() {
    // retriving product id from home page
    const productId = this.$route.query.id;
    // Make API request to fetch product information
    const data = fetch(`http://127.0.0.1:5000/manager/${productId}`,{
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
                this.message = data.message
                this.showMessage = true
                setTimeout(() => {
                    this.showMessage = false;
                }, 2000);
                }else if (data.Error){
                    console.log(data.Error)
                    this.message = data.Error;
                    this.showMessage = true
                }
                else {
                    this.product = data;
                }
                })
                .catch(error => {
                    console.error('Error:', error);
                })
                setTimeout(() => {
                        this.showMessage = false;
                    }, 2000);
  }
}
</script>

<style>


</style>