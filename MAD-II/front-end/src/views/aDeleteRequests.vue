<template>
    <div>
        <navbar :Role = 'Role'/>
        <div>
            <div class="navbar navbar-expand-lg navbar bg-custom"> 
                <div v-if="m" class="text-center mt-5" >
                    <h2>{{  m }}</h2> 
                </div>
                <subnavbar :Role = 'Role'/>
            </div>
        </div><br>
        <div> <h2>Request For Deleting Category</h2></div><br>
        <div v-if="e">
            <h2> {{ e }}</h2>
        </div>
        <div class="product-container">
            <div v-for= "i in list" :key="i.dr_id" >
                <div class="d-flex align-items-start bg-light mb-3" style="height: 100px;">
                    <div class="col-3" id="font">User Name : {{i.user_name}} </div>
                    <div class="col-2" id="font">Category Id : {{ i.category_id }} </div>
                    <div class="col-4" id="font">Catagory Name : {{i.catagory_name}} </div>
                    <button type="submit" class="btn btn-outline-secondary" @click="deleteCategory(i.dr_id)">Approve Request</button>&nbsp;
                    <button type="submit" class="btn btn-outline-danger" @click="deleteReq(i.dr_id)">Delete Request</button>
                </div>  
            </div>
        </div>
        <notification :show="showMessage" :message="message" />
        </div>
</template>
<script>
import subnavbar from '@/components/subnavbar.vue'
import navbar from '@/components/u_navbar.vue'
import notification from "@/components/notification.vue"

export default {
  components: {
    navbar,
    notification,
    subnavbar
  },
  data(){
    return {
        token: localStorage.getItem("auth_token"),
        Role: localStorage.getItem('role'),
        list:[],
        message: null,
        showMessage: false,
        e:null
    }
    },methods:{
        deleteReq(id){
            const isConfirm = window.confirm('Are You Sure You Want To Delete Request?')
            if (isConfirm){
                fetch(`http://127.0.0.1:5000/extra/${id}`,{
                method: 'put',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': this.token,
                },
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
                        window.location.reload()
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
                }, 5000);
            } 
        },
        deleteCategory(id){
            const isConfirm = window.confirm('Are You Sure You Want To Delete Category?')
            if (isConfirm){
                fetch(`http://127.0.0.1:5000//req_action`,{
                method: 'delete',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': this.token,
                },
                body: JSON.stringify({ dr_id : id })
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
                        window.location.reload()
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
                }, 5000);
            } 
        }
    },
    mounted(){
        fetch('http://127.0.0.1:5000/admin_req',{
            method: 'delete',
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
            if (data.message) {
              this.m = data.message
            }if (data.e) {
              this.e = data.e
            }else {
                this.list = data;
            }})
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
.bg-custom {
  background-color:rgb(241, 240, 240) ;
}
</style>