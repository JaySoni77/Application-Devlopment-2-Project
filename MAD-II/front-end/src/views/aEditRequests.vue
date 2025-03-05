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
        <div> <h2>Request For Editing In Category</h2></div><br>
        <div v-if="e">
            <h2> {{ e }}</h2>
        </div>
        <table v-else class="table table-striped larger-row">
            <thead>
                <th scope="col">Name:</th>
                <th scope="col">Category Name:</th>
                <th scope="col">Description:</th>
                <th scope="col">Message:</th>
                <th scope="col"></th>
            </thead>
            <tbody>
                <tr v-for= "i in list" :key="i.lr_id" class="larger-row">
                    <td>{{i.user_name}}</td>
                    <td>{{i.name}}</td>
                    <td>{{i.description}}</td>
                    <td>{{i.message}}</td>
                    <td><button type="submit" class="btn btn-outline-secondary" @click="editCat(i.category_id, i.name, i.description, i.request_id)">Approve Changes</button>&nbsp;</td>
                    <td><button type="submit" class="btn btn-outline-danger" @click="deleteReq(i.request_id)">Delete Request</button>&nbsp;</td>

                </tr>
            </tbody>
        </table>    
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
        e:null,
    }
    },methods:{
        editCat(category_id, name, description, request_id){
            const isConfirm = window.confirm('Are You Sure You Want To approve Changes?')
            if (isConfirm){
                fetch(`http://127.0.0.1:5000/req_action`,{
                method: 'put',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': this.token,
                },
                body: JSON.stringify({ name: name, d: description, rq_id:request_id, cId: category_id }),
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
                }else if (data.Error) {
                    this.message = data.Error
                    this.showMessage = true;
                    setTimeout(() => {
                        this.showMessage = false;
                    }, 3000);
                }
                else {
                    this.message = "Something Went Wrong!";
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
        deleteReq(id){
            const isConfirm = window.confirm('Are You Sure You Want To Delete Request?')
            if (isConfirm){
                fetch(`http://127.0.0.1:5000/delete_req/${id}`,{
                method: 'get',
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
        }
    },
    mounted(){
        fetch('http://127.0.0.1:5000/admin_req',{
            method: 'put',
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
            } if (data.e) {
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
.larger-row {
    height: 100px;
    font-size :x-large;
    font-style:oblique;
    font-variant: small-caps;
    color: #163d64;
}
</style>