<template>
    <div class="bg">
    <navbar :Role = 'Role'/>   
    <br>
    <button class="btn btn-outline-secondary" @click="createReq">Create Request</button>
    <div v-if="m" class="text-center mt-5" >
       <h2>{{  m }}</h2> 
    </div> 

    <div class="container mt-4">
        <div class="row">
        <div class="col-md-4" v-for="i in list" :key="list.catagory_id">
            <div class="card mb-3 ">
            <div class="card-body ct" >
                <h4 class="card-title">{{ i.name }}</h4><br>
                <p class="card-text">{{ i.description }}</p>
                <button @click="editRequest(i.catagory_id)" class="btn btn-outline-secondary">Edit Request</button>&nbsp;
                <button @click="deleteRequest(i.catagory_id)" class="btn btn-outline-secondary">Delete Request</button>
            </div>
            <notification :show="showMessage" :message="message"/>
            </div>
        </div>
        </div>
        </div>
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
    data() {
        return {
        list: [], 
        token: localStorage.getItem('auth_token'),
        Role: localStorage.getItem('role'),
        message: "",
        showMessage: false,
        m: "",
        };
    },
    methods:{
        editRequest(id){
               this.$router.push({path: '/mEditReq', query: { id }}) 
            },
        deleteRequest(id){
            const isConfirm = window.confirm("Are you sure You Want To Send A Request To Delete Category?")
            if (isConfirm){
                const data = fetch(`http://127.0.0.1:5000/manager_req/${id}`,{
            method: 'get',
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

            }else if (data.ErRoR){
                this.message = data.ErRoR;
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

        },
        createReq(){
            this.$router.push({path: '/mCreateReq'}) 
        }
        
    },
    mounted(){
            const data = fetch('http://127.0.0.1:5000/request',{
            method: 'get',
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
<style scoped>
.bg{
    min-height: 100vh;
    background-color: #f3f0f0;
}
.ct{
    background-color:rgb(230, 230, 230)
}
</style>