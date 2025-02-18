<template>
  <div class="app">
    <NavBar />
    <RouterView />
  </div>  
</template>

<script setup lang="ts">
  import NavBar from './components/NavBar.vue';
</script>

<style>
  .app {
    display: flex;
    flex-direction: column;
  }

  .navbar {
    border: 2px;
    border-color: red;
  }
</style>