<template>
    <div class="bg">
        <navbar :Role = 'Role'/>
        <div class="container mt-5 ">
            <div class="row justify-content-center">
              <div class="col-md-6">
                <div class="border p-4 rounded ca">
                    <h1 class="primary">Edit Category</h1>
                    <form @submit.prevent="editReq(list.name, list.description, list.catagory_id, reqMessage)">
                        <input v-model="list.name" class="form-control" type="text" placeholder="Name" required><br>
                        <input v-model="list.description" class="form-control" type="text" placeholder="Description" required><br>
                        <input v-model="reqMessage" class="form-control" type="text" placeholder="Your Message To Admin" required><br>
    
                        <button type="submit" class="btn btn-outline-success"> Send Edit Request <i class="bi bi-send-plus"></i> </button>&nbsp;
                        <button @click="goBack()" class="btn btn-outline-secondary">Back  <i class="bi bi-back"></i> </button>
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
        token: localStorage.getItem("auth_token"),
        Role: localStorage.getItem('role'),
        message: null,
        showMessage: false,
        list: "",
        reqMessage:""
    }},
    methods:{
        goBack(){
          this.$router.go(-1)  
        },
        async editReq(name, description, id, reqMessage){
            const data = fetch(`http://127.0.0.1:5000/manager_req`,{
            method: 'put',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            body: JSON.stringify({ name: name, d: description, id: id, reqMessage: reqMessage})
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
                  this.$router.push({ name: 'mRequestPage'});
                }, 2000);
                
            }else if (data.ErRoR){
                console.log(data.ErRoR)
                this.message = data.ErRoR;
                this.showMessage = true
            } else if (data.Error){
                    this.message = data.Error;
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
            }, 5000);
                        
        }
    },
    mounted(){
            const id = this.$route.query.id
            const data = fetch(`http://127.0.0.1:5000/request/${id}`,{
            method: 'put',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },
            // body: JSON.stringify( id )
            }).then(response => {
                if (!response.ok) {
                if (response.status === 403){this.$router.push({name:'forbidden'})}
                throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.ErRoR) {
                    // console.log(data.ErRor)
                    this.message = data.ErRoR;
                    this.showMessage = true
                    
                    
                }else if (data.error){
                    this.m = data.error;
                }
                else {
                this.list = data
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
.bg{
    min-height: 100vh;
    background-color: #eee;
}
.ca{
  background-color: rgb(242, 245, 248);
}
</style>

