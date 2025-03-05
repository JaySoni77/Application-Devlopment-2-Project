<template>
    <div>
        <navbar :Role = 'Role'/>
        <br><h1>Edit Product</h1>
        <div class="container  ">
            <div class="row justify-content-center">
                <div class="col-md-6">
                    <div class="border p-4 rounded ca">
                        <form @submit.prevent="editProduct">
                            Product Name:
                            <input type="text" class="form-control" placeholder="Product Name" v-model="p.name" required><br>
                            Price
                            <input type="number" class="form-control"  min="1" placeholder="Price" v-model="p.price" required><br>
                            Avalilable Quantity
                            <input type="number" class="form-control" placeholder="Avalilable Quantity" min="0" v-model="p.quantity" required><br>  
                            Unit
                            <input type="text" class="form-control" min="1" placeholder="Unit, e.g. = 2" v-model="p.unit" required><br>
                            Description
                            <input type="text" class="form-control" placeholder="Description" v-model="p.description" required><br>
                            
                            <div class="form-group row">
                                <label for="category" class="col-sm-3 col-form-label">Select Category:</label>
                                <select v-model="p.category" class="col-sm-9" required>
                                    <option value="" disabled>Select a category</option>
                                    <option v-for="c in categoryList" :key="c.catagory_id" :value="c.catagory_id">
                                        {{ c.name }}
                                    </option>
                                </select>
                            </div><br>
                            <div class="form-group row">
                                <label for="expiryDate" class="col-sm-3 col-form-label">Expiry Date:</label>
                                <div class="col-sm-9">
                                    <input type="date" id="expiryDate" class="form-control" v-model="p.expiryDate" :min="minDate" required>
                                </div>
                            </div><br>
                            <div class="form-group row">
                                <label class="col-sm-3 col-form-label">Product Image:</label>
                                <div class="col-sm-9">
                                    <input type="file" id="image" class="form-control" v-on:change="img">
                                </div>
                            </div><br>
                            
                            <button type="submit" class="btn btn-outline-secondary">Save Changes  <i class="bi bi-floppy"></i></button>&nbsp;
                            <button @click="goBack()" class="btn btn-outline-secondary"> Back  <i class="bi bi-back"></i> </button>

                        </form>
                    </div>
                <notification :show="showMessage" :message="message" />
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
                p:{
                    product_id:null,
                    name:null,
                    price:null,
                    quantity:null,
                    unit:null,
                    category:null,
                    expiryDate:null,
                    description:null,
                },
                
                token: localStorage.getItem('auth_token'),
                Role: localStorage.getItem('role'),
                message: "",
                showMessage: false,
                categoryList:[],
                product: [],
                minDate:null,
            }
        },
        methods: {
            setMinDate(){
                this.minDate = new Date().toISOString().split('T')[0];
            },
            goBack(){
                this.$router.go(-1)  
            },
            img(event) {
                this.p.image = event.target.files[0];
            },
            editProduct(){
            
            const formData = new FormData();
            for (const key in this.p) {
                formData.append(key, this.p[key]);
            }
            formData.append('image', this.p.image);
            
            const data = fetch(`http://127.0.0.1:5000/productCRUD`,{
            method: 'put',
            headers: {
              'Authorization': this.token, 
            },
            body: formData
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
                    this.$router.push({ name: 'mHome'});
                }, 2000);
                
            }else if (data.Error){
                console.log(data.Error)
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
                }, 2000);
        }
    },
    mounted(){
        this.setMinDate()
        fetch('http://127.0.0.1:5000/extra',{
        method: 'post',
        headers:{
            'Content-type': 'application/json',
            'Authorization': this.token,
        }
        }).then(response => {
            if (!response.ok) {
                if (response.status === 403){this.$router.push({name:'forbidden'})}
                throw new Error('Network response was not ok');
                }
             return response.json()})
        .then(data => {
        if (data) {
          this.categoryList = data;
        } else {
            this.m = "Cart Is Empty"; // Set the message from the response
        }})
        .catch (Error => {console.log ("Error :" , Error)});

        ////////////////////////////////////////////////////

        // another fetch request
        const productId = this.$route.query.productId;
        const data = fetch(`http://127.0.0.1:5000/manager/${productId}`,{
            method: 'put',
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
        if (data.message) {
        this.message = data.message
        this.showMessage = true
        setTimeout(() => {
            this.showMessage = false;
        }, 2000);
        }else if (data.Error){
            console.log(data.Error)
            this.message = data.Error;
            this.showMessage = true
        }
        else {
            this.p.product_id = data.product_id
            this.p.name = data.name;
            this.p.price = data.price;
            this.p.quantity = data.quantity;
            this.p.unit = data.unit;
            this.p.description = data.description;
            this.p.category = data.catagory_id;
            this.p.expiryDate = data.expiry_date;
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