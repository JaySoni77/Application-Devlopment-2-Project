<template>
    <div class="bg">
        <navbar :Role = 'Role'/>
        <div class="container mt-5 ">
            <div class="row justify-content-center">
              <div class="col-md-6">
                <div class="border p-4 rounded ca">
                    <h1 class="primary">Add Category</h1>
                    <form @submit.prevent="createCategory">
                      <input v-model="category.name" class="form-control" type="text" placeholder="Name" required><br>
                      <input v-model="category.description" class="form-control" type="text" placeholder="Description" required><br>
                      <button type="submit" class="btn btn-outline-success"> Create Category </button>&nbsp;
                      <button @click="goBack()" class="btn btn-outline-secondary">Back <i class="bi bi-back"></i></button>
                    </form>
                </div>
              </div>
                <notification :show="showMessage" :message="message" />
            </div>
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
    data(){
        return{
        category:{
            name: null,
            description: null},
        token: localStorage.getItem("auth_token"),
        Role: localStorage.getItem('role'),
        message: null,
        showMessage: false
    }},
    methods:{
        goBack(){
          this.$router.go(-1)  
        },
        createCategory(){
            const data = fetch(`http://127.0.0.1:5000/categoryCRUD`,{
            method: 'post',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify( this.category )
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
                this.$router.push({ name: 'aHome'});
              }, 2000);
              
          }else if (data.ErRor){
            console.log(data.ErRor)
            this.message = data.ErRor;
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
                        
        }
    }
}
</script>
<style>
.bg{
    min-height: 100vh;
    background-color: #eee;
}
.ca{
  background-color: rgb(242, 245, 248);
}
</style>

