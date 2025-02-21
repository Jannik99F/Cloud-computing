<template>
  <div class="app">
    <div class="navbar">
    <NavBar />
  </div>
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
    padding: 1rem;
  }
</style>
