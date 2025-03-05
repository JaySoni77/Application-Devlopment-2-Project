<template>
    <div>
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
                  <h2 class="fw-bold mb-5">Request Admin to Grant "Manager"  Role</h2>
                    <form @submit.prevent="req">
                      <div>
                        <div class="form-outline mb-4">
                          <input type="email" v-model="list.email" class="form-control" placeholder="Email address"  required/>
                        </div>
            
                        <div class="form-outline mb-4">
                          <input type="password" class="form-control" placeholder="Password" v-model="list.password" required/>
                        </div>
                        
                        <div class="form-outline mb-4">
                          <input type="text" class="form-control" placeholder="Your Message To Admin" v-model="list.message" required/>
                        </div>
    
                        <!-- Error message -->
                        <div class="text-danger mb-4">{{ error }}</div>
            
                        <!-- Submit button -->
                        <button type="submit" class="btn btn-outline-secondary ">Request</button>
                      </div>
                    </form>
                </div>
              </div>
            </div>
          </div>
        </section>
    </div>
  </template>
  
  <script>
  export default {
    data() {
      return {
        list: {
          email: null,
          password: null,
          message: null
        },
        error: null,
        message: null,
      };
    },
    methods: {
      async req() {
        const res = await fetch(`http://127.0.0.1:5000/req`, {
          method: 'post',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.list),
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
              this.showMessage = true
              setTimeout(() => {
                this.showMessage = false;
                this.$router.push({ name: 'login'});
              }, 4000);
              
          }else if (data.Error){
            console.log(data.Error)
            this.error = data.Error;
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
    },
  },
};
</script>
  