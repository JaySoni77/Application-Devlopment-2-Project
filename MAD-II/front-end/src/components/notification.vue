<!-- Notification.vue -->
<template>
    <div v-if="show" class="notification">
      <p>{{ message }}</p>
    </div>
</template>
  
<script>
  export default {
    props: {
      show: Boolean,
      message: String,
    },
  };
</script>
  
<style>
  .notification {
    position:fixed ;
    top: 80%;
    left: 50%;
    transform: translate(-50%, -50%);
    background-color: #cdd0cd;
    color: #130101;
    padding: 15px;
    border-radius: 5px;
    display: inline-block;
    max-width: 500px;
  }
</style>
  