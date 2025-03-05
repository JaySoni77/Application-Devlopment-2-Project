import { createRouter, createWebHashHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import login from '../views/login.vue'
import u_home from '../views/u_home.vue'
import u_product from '../views/u_product.vue'
import cart from '../views/cart.vue'
import deliveryDetails from '../views/deliveryDetails.vue'
import order from '../views/order.vue'
import u_category from '../views/u_category.vue'
import u_product_by_category from '../views/u_product_by_category'
import mHome from '../views/mHome'
import mProduct from '../views/mProduct'
import mStock from '../views/mStock'
import mAllOrders from '../views/mAllOrders'
import signup from '../views/signup.vue'
import mAddProduct from '../views/mAddProduct'
import mViewOrder from '../views/mViewOrder'
import aHome from '../views/aHome'
import aAddCategory from '../views/aAddCategory'
import aAllUsers from '../views/aAllUsers.vue'
import aEditCategory from '../views/aEditCategory'
import mRequestPage from '../views/mRequestPage'
import mEditReq from '../views/mEditReq'
import mCreateReq from '../views/mCreateReq.vue'
import mSignup from '../views/mSignup.vue'
import mEditProduct from '../views/mEditProduct'
import aRoleApproval from '../views/aRoleApproval.vue'
import aCreateRequest from '../views/aCreateRequest.vue'
import aEditRequests from '../views/aEditRequests.vue'
import aDeleteRequests from '../views/aDeleteRequests.vue'
import aViewCreateRequest from '../views/aViewCreateRequest.vue'
import adminSearch from '../views/adminSearch.vue'
import managerSearch from '../views/managerSearch.vue'
import userSearch from '../views/userSearch.vue'
import uViewOrder from '../views/uViewOrder.vue'
import forbidden from '../views/403.vue'

const routes = [
  // { path: '/xyz',name: 'home',component: HomeView },
  { path: '/about', name: 'about',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: function () {
      return import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    }
  },
  { path: '/', name: 'login', component: login },
  { path: '/signup', name: 'signup', component: signup },
  { path: '/mSignup', name: 'mSignup', component: mSignup },
  { path: '/forbidden', name: 'forbidden', component: forbidden },

  //user route
  { path: '/user_home', name: 'u_home', component: u_home },
  { path: '/u_product', name: 'u_product', component: u_product },
  { path: '/cart', name: 'cart', component: cart },
  { path: '/deliveryDetails', name: 'deliveryDetails', component: deliveryDetails },
  { path: '/order', name: 'order', component: order },
  { path: '/u_category', name: 'u_category', component: u_category },
  { path: '/u_product_by_category', name: 'u_product_by_category', component: u_product_by_category },
  { path: '/userSearch', name: 'userSearch', component: userSearch },
  { path: '/uViewOrder', name: 'uViewOrder', component: uViewOrder },
  
  //manager route
  { path: '/mHome', name: 'mHome', component: mHome },
  { path: '/mProduct', name: 'mProduct', component: mProduct },
  { path: '/mStock', name: 'mStock', component: mStock },
  { path: '/mAllOrders', name: 'mAllOrders', component: mAllOrders },
  { path: '/mAddProduct', name: 'mAddProduct', component: mAddProduct },
  { path: '/mEditProduct', name: 'mEditProduct', component: mEditProduct },
  { path: '/mViewOrder', name: 'mViewOrder', component: mViewOrder },
  { path: '/mRequestPage', name: 'mRequestPage', component: mRequestPage },
  { path: '/mEditReq', name: 'mEditReq', component: mEditReq },
  { path: '/mCreateReq', name: 'mCreateReq', component: mCreateReq },
  { path: '/managerSearch', name: 'managerSearch', component: managerSearch },
  
  
  //Admin route
  { path: '/aHome', name: 'aHome', component: aHome },
  { path: '/aAddCategory', name: 'aAddCategory', component: aAddCategory },
  { path: '/aAllUsers', name: 'aAllUsers', component: aAllUsers },
  { path: '/aEditCategory', name: 'aEditCategory', component: aEditCategory },
  { path: '/aRoleApproval', name: 'aRoleApproval', component: aRoleApproval },
  { path: '/aCreateRequest', name: 'aCreateRequest', component: aCreateRequest },
  { path: '/aDeleteRequests', name: 'aDeleteRequests', component: aDeleteRequests },
  { path: '/aEditRequests', name: 'aEditRequests', component: aEditRequests },
  { path: '/aViewCreateRequest', name: 'aViewCreateRequest', component: aViewCreateRequest },
  { path: '/adminSearch', name: 'adminSearch', component: adminSearch },


  
]

const router = createRouter({
  history: createWebHashHistory(),
  routes
})

export default router
