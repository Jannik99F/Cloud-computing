<template>
  <div class="app">
    <header class="navbar">
      <NavBar />
    </header>
    <header class="user-and-basket-bar">
      <UserAndBasket />
    </header>
    <main class="content">
      <RouterView />
    </main>
  </div>  
</template>

<script setup lang="ts">
  import NavBar from './components/NavBar.vue';
import UserAndBasket from './components/UserAndBasket.vue';
</script>

<style>
  .app {
    display: flex;
    flex-direction: column;
  }

  .navbar {
    position: fixed;
    top: 0;
    left: 0;
    padding: 20px;
  }

  .user-and-basket-bar {
    position: fixed;
    top: 0;
    right: 0;
    padding: 20px;
  }

  .content {
    margin-top: 40px;
    padding: 20px;
}
</style>
