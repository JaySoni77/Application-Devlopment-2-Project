<template>
    <div class="bg">
        <navbar :Role = 'Role'/>
        <div v-if="m" class="text-center mt-5">
            <h2>{{  m }}</h2> 
        </div>
        <div v-else class="container mt-4">
        <div class="row">
        <div class="col-md-4" v-for="i in list" :key="list.catagory_id">
            <div class="card mb-3 ">
            <div class="card-body ct" >
                <h4 class="card-title">{{ i.name }}</h4><br>
                <p class="card-text">{{ i.description }}</p>
                <button @click="editCategory(i.catagory_id)" class="btn btn-outline-secondary">Edit Category</button>&nbsp;
                <button @click="deleteCategory(i.catagory_id)" class="btn btn-outline-secondary">Delete Category</button>
            </div>
            <notification :show="showMessage" :message="message" />
        <!-- <div class="text-primary mb-4">{{ this.$route.query.message }}</div> -->

            </div>
        </div>
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
                token: localStorage.getItem('auth_token'),
                Role: localStorage.getItem('role'),
                list: [],
                message: null,
                showMessage: false,
                m:null,
            }
        },
        methods:{
            editCategory(categoryId){
               this.$router.push({path: '/aEditCategory', query: { categoryId }}) 
            },
            deleteCategory(catagoryId){
                const isConfirm = window.confirm("Are You Sure You Want To Delete Category?")
                if (isConfirm){
                    const data = fetch(`http://127.0.0.1:5000/categoryCRUD`,{
                    method: 'delete',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': this.token, 
                    },
                    body: JSON.stringify({ catagoryId })
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
                                    window.location.reload();
                            }, 3000);                        
                    }else if (data.Error){
                        console.log(data.Error)
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
                }
            }
        },
    mounted(){
        const aQuery = this.$route.query.aQuery
        console.log(aQuery)
        const data = fetch(`http://127.0.0.1:5000/searchQuery`,{
            method: 'post',
            headers: {
              'Content-Type': 'application/json',
              'Authorization': this.token, 
            },body: JSON.stringify({aQuery: aQuery}),
            }).then(response => {
                if (!response.ok) {
                    if (response.status === 403){this.$router.push({name:'forbidden'})}
                throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                if (data.no_result) {
                    this.m = data.no_result;
                }else if(data.Error){
                    this.message.data.Error
                    this.showMessage = true
                    setTimeout(() => {
                        this.showMessage = false;
                    }, 3000);
                }   else {
                    this.list = data;
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
    background-color: #eee;
}
.ct{
    background-color:rgb(230, 230, 230)
}
</style>
