<template>
  <div class="app">
    <div class="headers">
      <header class="navbar">
        <NavBar />
      </header>
      <header class="login-info">
        <LoginInfo />
      </header>
      <header class="user-and-basket-bar">
        <UserAndBasket />
      </header>
    </div>
    <main class="content">
      <RouterView />
    </main>
  </div>
</template>

<script setup lang="ts">
  import NavBar from './components/NavBar.vue';
  import UserAndBasket from './components/UserAndBasket.vue';
  import LoginInfo from './components/LoginInfo.vue';
</script>

<style>
  .app {
    display: flex;
    flex-direction: column;
  }

  .headers {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: center;
    position: fixed;
    top: 0;
    width: 100%;
    padding: 30px;
  }

  .navbar {
    position: fixed;
    left: 0;
  }

  .login-info {
    position: fixed;
    left: 50%;
    transform: translateX(-50%);
  }

  .user-and-basket-bar {
    position: fixed;
    right: 0;
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
