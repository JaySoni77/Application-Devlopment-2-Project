<template>
  <div >
    <navbar :Role = 'Role'/>
    <div class="container mt-5 ">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="border p-4 rounded ca">
    <h2><div class="light">Delivery Details</div></h2>
    <form @submit.prevent="placeOrder">
      <div>
        <div>
          <input v-model="receiver" type="text" class="form-control" placeholder="Enter Your Name" required><br>
          <input v-model="address" type="text" class="form-control" placeholder="Enter Your Address" required><br>
          <input v-model="city" type="text" class="form-control" placeholder="Enter City" required><br>
          <input v-model="state" type="text" class="form-control" placeholder="Enter State" required><br>
          <input v-model="pincode" type="number" class="form-control" placeholder="Enter Pincode" required><br>
          <input v-model="contactNumber" type="number" class="form-control" placeholder="Contact Number" required><br>
        </div><br>
        <button type="submit" class="btn btn-warning" style="width:200px">Place Your Order</button>
      </div>
    </form>
  </div>
  </div>
  </div>
  </div><br>
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
    data(){
        return{
            token: localStorage.getItem('auth_token'),
            Role: localStorage.getItem('role'),
            receiver: "",
            address: "",
            city: "",
            state: "",
            pincode: "",
            contactNumber: "",
            message: "",
            showMessage: false,
            m: "",
        };
    },
    
    methods: {
        placeOrder() {
            const info = { 
            receiver: this.receiver,
            address: this.address,
            city: this.city,
            state: this.state,
            pincode: this.pincode,
            contactNumber: this.contactNumber,
            }
            fetch('http://127.0.0.1:5000/buy',{
            method: 'post',
            headers:{
                'Content-type': 'application/json',
                'Authorization': this.token,
            },
            body: JSON.stringify({ info })
            }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }else if (response.status === 201){
                this.message = "Ordered amount is grater than availabel quantity!", 
                this.showMessage = true
                setTimeout(() => {
                this.showMessage = false;
                this.$router.push({ name: 'cart' });
              }, 2000);

            }
            return response.json();
            })
            .then(data => {
              if(data.Error){
              this.message = data.Error,
              this.showMessage = true
              setTimeout(() => {
                this.showMessage = false;
              }, 2000);
            }else if (data){
                this.message = data, 
                this.showMessage = true
                setTimeout(() => {
                this.showMessage = false;
                this.$router.push({ name: 'order' });
              }, 2000);
              }})
            .catch (Error => {console.log ("Error :" , Error)})

        }
    },
        
  };
</script>