<template>
    <div >

    </div>
    <div v-if="Role === 'User' ">
        <div class="jumbotron">
                <h1>Nature'sNourish</h1>
                <h4>"Nature's Goodness in Every Aisle."</h4>
            </div>
        <div>
        <nav class="navbar navbar-expand-lg navbar bg-custom">
        <div class="container-fluid">
        <em><b><b>Brand</b></b></em>&nbsp;
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarCollapse">
            <div class="navbar-nav">
                <router-link to="/user_home" class="nav-item nav-link">Home  <i class="bi bi-house-door-fill"></i></router-link>
                <router-link to="/u_category" class="nav-item nav-link">Categories <i class="bi bi-card-list"></i></router-link>
                <router-link to="/order" class="nav-item nav-link">Your Orders <i class="bi bi-bag-plus"></i></router-link>
                <router-link to="/cart" class="nav-item nav-link"> Cart  <i class="bi bi-cart"></i></router-link>

            </div>
            <div class="col-7">
                <form @submit.prevent="userSearch">
                        <div class="input-group">
                        <input v-model="uQuery" type="text" class="form-control" placeholder="  Search Product By Name" required>&nbsp;
                        <input v-model="price" type="number" class="form-control" placeholder="  Upper Limit Of Price">
                        <button type="submit" class="btn btn-secondary">  <i class="bi bi-search"></i></button>
                    </div>
                </form>
            </div>
            <div class="navbar-nav">
            
            <button @click="logout" class="nav-item nav-link btn btn-link">Logout  <i class="bi bi-box-arrow-right"></i></button>
            </div>
        </div>
        </div>
    </nav>
    </div>

    </div>
    

    <div v-if="Role === 'Admin' ">
        <div class="jumbotron">
                <h1>Nature'sNourish</h1>
                <h4>"Nature's Goodness in Every Aisle."</h4>
                <div class="container-fluid "><h5><em>Admin's Panel</em></h5></div>

            </div>
        <div>
        <nav class="navbar navbar-expand-lg navbar bg-custom"> <!-- Change background color to your desired color -->
        <div class="container-fluid">
        <router-link to="/" class="navbar-brand">Brand</router-link>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarCollapse">
            <div class="navbar-nav">
            <router-link to="/aHome" class="nav-item nav-link">Home  <i class="bi bi-house-door-fill"></i></router-link>
            <router-link to="/aAddCategory" class="nav-item nav-link">Add Category <i class="bi bi-file-earmark-plus"></i></router-link>
            <router-link to="/aRoleApproval" class="nav-item nav-link">View Requests  <i class="bi bi-card-checklist"></i></router-link>
            <!-- <router-link to="/profile" class="nav-item nav-link">Profile</router-link> -->

            </div>
            <div class="col-8">
                <form @submit.prevent="adminSearch()">
                        <div class="input-group">
                        <input type="text" v-model="aQuery" class="form-control" placeholder="  Search Category By Name" required>
                        <button type="submit" class="btn btn-secondary">Search</button>
                    </div>
                </form>
            </div>
            <div class="navbar-nav">
            
            <button @click="logout" class="nav-item nav-link btn btn-link">Logout  <i class="bi bi-box-arrow-right"></i></button>
            </div>
        </div>
        </div>
    </nav>
    </div>

    </div>
    
    <div v-if="Role === 'storeManager'">
        <div class="jumbotron">
                <h1>Nature'sNourish</h1>
                <h4>"Nature's Goodness in Every Aisle."</h4>
                <div class="container-fluid "><h5><em>Manager's Panel</em></h5></div>
            </div>
    <div>
        <nav class="navbar navbar-expand-lg navbar bg-custom"> <!-- Change background color to your desired color -->
        <div class="container-fluid">
            <router-link to="/" class="navbar-brand">Brand</router-link>
        <button type="button" class="navbar-toggler" data-bs-toggle="collapse" data-bs-target="#navbarCollapse">
            <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse justify-content-between" id="navbarCollapse">
            <div class="navbar-nav">
            <router-link to="/mHome" class="nav-item nav-link">Home <i class="bi bi-house-door-fill"></i></router-link>
            <!-- <router-link to="/profile" class="nav-item nav-link">Profile</router-link> -->
            <router-link to="/mStock" class="nav-item nav-link">Out of Stock  <i class="bi bi-cart-x"></i></router-link>
            <router-link to="/mAllOrders" class="nav-item nav-link">All Orders  <i class="bi bi-card-list"></i></router-link>
            <router-link to="/mAddProduct" class="nav-item nav-link">Add Product  <i class="bi bi-bag-plus"></i></router-link>
            <router-link to="/mRequestpage" class="nav-item nav-link">Request Page  <i class="bi bi-pencil-square"></i></router-link>
            
            <!-- <div class="navbar-nav">
            <div class="nav-item dropdown">
                <a href="#" class="nav-link dropdown-toggle" data-bs-toggle="dropdown">Actions</a>
                <div class="dropdown-menu">
                    <router-link to="/inbox" class="dropdown-item">Inbox</router-link>
                    <router-link to="/sent" class="dropdown-item">Sent</router-link>
                    <router-link to="/drafts" class="dropdown-item">Drafts</router-link>
                    <router-link to="/add-products" class="nav-item nav-link">Add Products</router-link>
                </div>
            </div>
            </div> -->

            </div>
            <div class="col-6">
                <form @submit.prevent="managerSearch">
                        <div class="input-group">
                        <input v-model="mQuery" type="text" class="form-control" placeholder="  Searchby name" required>&nbsp;
                        <input v-model="price" type="number" class="form-control" placeholder="  Upperlimit of price">
                        <button type="submit" class="btn btn-secondary">Search</button>
                    </div>
                </form>
            </div>
            <div class="navbar-nav">
            
            <button @click="logout" class="nav-item nav-link btn btn-link">Logout <i class="bi bi-box-arrow-right"></i></button>
            </div>
        </div>
        </div>
    </nav>
    </div>

    </div>

</template>
<script>
    
    export default{
        
        props: {
            Role: {
            type: String,
            required: true,
            }
        },
        data(){
        return{
            'token': localStorage.getItem('auth_token'),
            'role' : localStorage.getItem('role'),
            aQuery:null,
            mQuery:null,
            price:null,
            uQuery:null,

        }
    },
    computed : {
        shouldRenderNavbar(){
            return this.$route.name !== 'login';
        }
    },
    methods : {
        logout(){
            localStorage.removeItem('auth_token')
            localStorage.removeItem('role')
            this.$router.push('/')

        },
        adminSearch(){
                this.$router.push({name: 'adminSearch', query:{ aQuery: this.aQuery }})
                window.location.reload
        },managerSearch(){
           this.$router.push({name: 'managerSearch', query:{ mQuery: this.mQuery, price: this.price }})
           window.location.reload
        },userSearch(){
           this.$router.push({name: 'userSearch', query:{ uQuery: this.uQuery, price: this.price }})
           window.location.reload
   }
    }
}   
</script>
<style scoped>
.bg-custom {
  background-color:gainsboro ;
}

      .navbar {
      margin-bottom: 50px;
      border-radius: 0;
      /* background-color: rgb(21, 2, 55); */
      }

      .jumbotron {
          margin-bottom: 0;
          background-color: rgb(255, 255, 255);
          padding: 15px 0;
      }
      .navbar {
          margin-bottom: 0 !important;
      }

</style>