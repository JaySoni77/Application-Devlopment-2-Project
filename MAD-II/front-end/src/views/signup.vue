<template>
    <section class="text-center">
      <div class="p-5 bg-image" style="
              background-image: url('https://mdbootstrap.com/img/new/textures/full/171.jpg');
              height: 300px;"></div>
  
      <div class="card mx-4 mx-md-5 shadow-5-strong" style="
              margin-top: -100px;
              background: hsla(0, 0%, 100%, 0.8);
              backdrop-filter: blur(30px);
              ">
        <div class="card-body py-5 px-md-5">
        <div class="text-primary mb-4"> {{ message }}</div>
          <div class="row d-flex justify-content-center">
            <div class="col-lg-8">
              <h2 class="fw-bold mb-5">Sign Up</h2>
                <form @submit.prevent="Signup">
                  <div>
                    <div class="form-outline mb-4">
                      <input type="text" class="form-control" placeholder="Enter Your Name" v-model="credentials.name" required/>
                    </div>

                    <div class="form-outline mb-4">
                      <input type="email" v-model="credentials.email" class="form-control" placeholder="Email address"  required/>
                    </div>
        
                    <div class="form-outline mb-4">
                      <input type="password" class="form-control" placeholder="Password" v-model="credentials.password" required/>
                    </div>
                    
                    <div class="form-outline mb-4">
                      <input type="password" class="form-control" placeholder="Confirm Password" v-model="credentials.confirmPassword" required/>
                    </div>

                    <!-- Error message -->
                    <div class="text-danger mb-4">{{ error }}</div>
        
                    <!-- Submit button -->
                    <button type="submit" class="btn btn-info btn-block mb-4">Signup</button>
                  </div>
                </form>
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
          name: null,
          email: null,
          password: null,
          confirmPassword: null
        },
        error: null,
        message: null,
      };
    },
    methods: {
      async Signup() {
        const res = await fetch('http://127.0.0.1:5000/custom_login', {
          method: 'put',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.credentials),
        });
        const data = await res.json();
        if (res.ok) {
        this.message = data.message;
        this.$router.push({ name: 'login', query: { message: this.message } });

      } else {
        this.error = data.message;
      }
    },
  },
};
</script>
  