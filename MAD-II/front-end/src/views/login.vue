<template>
    <section class="text-center">
      <!-- Background image -->
      <div class="p-5 bg-image" style="
              background-image: url('https://mdbootstrap.com/img/new/textures/full/171.jpg');
              height: 300px;"></div>
      <!-- Background image -->
  
      <div class="card mx-4 mx-md-5 shadow-5-strong" style="
              margin-top: -100px;
              background: hsla(0, 0%, 100%, 0.8);
              backdrop-filter: blur(30px);
              ">
        <div class="card-body py-5 px-md-5">
          
          <div class="text-primary mb-4">{{ this.$route.query.message }}</div>
          <div class="row d-flex justify-content-center">
            <div class="col-lg-8">
              <h2 class="fw-bold mb-5">Login</h2>
  
              <div class="form-outline mb-4">
                <input type="email" class="form-control" placeholder="Email address" v-model="credentials.email" />
              </div>
  
              <div class="form-outline mb-4">
                <input type="password" class="form-control" placeholder="Password" v-model="credentials.password"/>
              </div>
  
              <div class="text-danger mb-4">{{ error }}</div>
  
              <button type="button" class="btn btn-outline-success btn-block mb-4" @click="loginuser">
                Log in
              </button><br>
              
            </div>
            <div>
              <b>New user?  click here to</b> <router-link to="/signup" class="nav-link text-primary mb-4"><b>Signup.</b></router-link>
            </div>
            <div>
              <b>Click here for</b> <router-link to="/mSignup" class="nav-link text-primary mb-4"><b> Manager Signup.</b></router-link>
            </div>
          </div>
        </div>
      </div>
    </section>
  </template>
  
  <script>
  export default {
    data() {
      return {
        credentials: {
          email: null,
          password: null,
        },
        error: null,
        message: null
      };
    },
    methods: {
      async loginuser() {
        const res = await fetch('http://127.0.0.1:5000/custom_login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.credentials),
        });
        const data = await res.json();
        if (res.ok) {
        localStorage.setItem('auth_token', data.Token);
        localStorage.setItem('role', data.Role);

        if (data.Role === 'User') {
          this.$router.push({ path: '/user_home' });
        } else if (data.Role === 'Admin') {
          this.$router.push({ path: '/aHome' });
        } else if (data.Role === 'storeManager') {
          this.$router.push({ path: '/mhome' });
        }
      } else {
        this.error = data.message;
      }
    },
  },
  mounted() {
    this.message = this.$route.query.message;
  }
};
</script>
  