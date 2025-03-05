<template>
    <div>
        <div >
        <navbar :Role = 'Role'/>
        <div>
            <h2>Your Orders</h2>
        </div><br>
    
        <table  class="table table-striped larger-row">
            <thead>
                <th scope="col">Receiver:</th>
                <th scope="col">Order ID:</th>
                <th scope="col">Total:</th>
                <th scope="col">Order Date:</th>
                <th scope="col">Status:</th>
                <th scope="col"></th>
            </thead>
            <tbody>
                    <tr v-for="i in row" :key="i.order_id" class="larger-row">
                        <td>{{ i.receiver }}</td>
                        <td>{{ i.order_id }}</td>
                        <td>{{ i.total }}</td>
                        <td>{{ i.order_date }}</td>
                        <td>{{ i.status }}</td>
                        <td><button @click="viewProduct(i.order_id)" class="btn btn-outline-secondary">view Order</button>&nbsp;</td>
                    </tr>
            </tbody>

        </table>
        <notification :show="showMessage" :message="message" />
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
                message: "" ,
                showMessage: false,
                Role: localStorage.getItem('role'),
                row:[],
                token: localStorage.getItem('auth_token'),
            }
        },
        methods:{
           viewProduct(id){
                this.$router.push({name: 'uViewOrder', query:{ id }})
           } 
        },
        mounted() {            
            const data = fetch(`http://127.0.0.1:5000/req`,{
            method: 'get',
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
                    this.message = data.message; // Set the message from the response
                } else {
                    this.row = data;
            }
            })
            .catch(error => {
                console.error('Error:', error);
            }); 
    }
  };
  </script>
<style>
.larger-row {
    height: 100px;
    font-size :x-large;
    font-style:oblique;
    font-variant: small-caps;
    color: #163d64;
}

</style>