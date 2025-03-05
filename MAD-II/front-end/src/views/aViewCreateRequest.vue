<template>
    <div class="bg">
        <navbar :Role = 'Role'/>
        <div class="container mt-5 ">
            <div class="row justify-content-center">
              <div class="col-md-6">
                <div class="border p-4 rounded ca">
                    <h1 class="primary">Add Category</h1><br>
                    <div> Request By: {{ cat.user_name }} </div><br>
                    <div> Message : {{ cat.m }} </div><br>
                    <form @submit.prevent="createCategory">
                      <input v-model="cat.name" class="form-control" type="text" placeholder="Name" required><br>
                      <input v-model="cat.description" class="form-control" type="text" placeholder="Description" required><br>
                      <button type="submit" class="btn btn-outline-success"> Create Category </button>&nbsp;
                    </form>
                    <button @click="goBack()" class="btn btn-outline-secondary">Back <i class="bi bi-back"></i> </button>
                </div>
              </div>
                <notification :show="showMessage" :message="message" />
            </div>
        </div>
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
        token: localStorage.getItem("auth_token"),
        Role: localStorage.getItem('role'),
        list:[],
        message: null,
        showMessage: false,
        cat:{
            user_name:null,
            name:null,
            description:null,
            m:null,
            request_id: null,
        },
    }
    },methods:{
        createCategory(){
            const isConfirm = window.confirm('Are You Sure You Want Create A Category?')
            if (isConfirm){
                fetch(`http://127.0.0.1:5000/req_action`,{
                method: 'post',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': this.token,
                },
                body: JSON.stringify({ name:this.cat.name, description: this.cat.description, id:this.cat.request_id }),
                })
                .then(response => {
                if (!response.ok) {
                throw new Error('Network response was not ok');
                }
                return response.json();
                })
                .then(data => {
                if (data.message) {
                    this.message = data.message
                    this.showMessage = true;
                    setTimeout(() => {
                        this.showMessage = false;
                        this.$router.push({path: '/aCreateRequest'})

                    }, 3000);
                }else {
                    this.message = data.Error;
                    this.showMessage = true;

                }})
                .catch(error => {
                    console.error('Error:', error);
                })
                setTimeout(() => {
                        this.showMessage = false;
                }, 3000);
            } 
        },
        goBack(){
            this.$router.go(-1)
        }
    },
    mounted(){
        const id = this.$route.query.id
        fetch(`http://127.0.0.1:5000/extra/${id}`,{
            method: 'get',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': this.token,
            },
            })
            .then(response => {
            if (!response.ok) {
                if (response.status === 403){this.$router.push({name:'forbidden'})}
              throw new Error('Network response was not ok');
            }
            return response.json();
            })
            .then(data => {
            if (data) {
                this.cat.name = data.name,
                this.cat.user_name = data.user_name,
                this.cat.description = data.description,
                this.cat.m = data.message;
                this.cat.request_id = data.request_id;

            }if(data.e){
                    this.message = data.e
                    this.showMessage = true;
                    setTimeout(() => {
                        this.showMessage = false;

                    }, 3000);
            }
        })
            .catch(error => {
                console.error('Error:', error);
            })
    }
}
</script>
<style>
.bg-custom {
  background-color:rgb(241, 240, 240) ;
}
</style>