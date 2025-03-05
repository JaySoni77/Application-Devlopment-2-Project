<template>
    <div>
        <navbar :Role = "Role"/>
        <div class="product-container">
            <div v-for= "u in users" :key="u.u_id" >
                <div class="d-flex align-items-start bg-light mb-3" style="height: 100px;">
                    <div class="col" id="font">Name : {{u.name}} </div>
                    <div class="col" id="font">Role : {{u.role}} </div>
                    <div class="col" id="font">Email : {{u.email}} </div>
                    <button @click="" class="btn btn-outline-success">Grant Role</button>
                    <button @click="" class="btn btn-outline-danger">Remove Role</button>

                </div>  
                <notification :show = "showMessage" :message = "message"/>
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
        data(){
            return{
                users: null,
                Role: localStorage.getItem('role'),
                token: localStorage.getItem("auth_token"),
                showMessage: false,
                message: null,
            }
        },
        mounted(){
            fetch('http://127.0.0.1:5000/admin',{
            method: 'GET',
            headers:{
                'Content-type': 'application/json',
                'Authorization': this.token,
            }
            }).then(response => {
            if (!response.ok) {
              throw new Error('Network response was not ok');
            }
            return response.json();
            })
            .then(data => {
            if (data.ErRoR){
                console.log(data.ErRoR)
                this.message = "Opps Something Went Wrong";
                this.showMessage = true
            }else if (data) {
                this.users = data.message     
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
              }, 7000); 
        }}
</script>