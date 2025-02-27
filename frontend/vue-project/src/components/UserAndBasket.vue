<template>
    <nav v-if="(isUserLoggedIn())">
        <RouterLink to="/basket">Basket</RouterLink>
        <RouterLink to="/logout">Logout</RouterLink>
    </nav>
    <nav v-else>
        <RouterLink to="/basket">Basket</RouterLink>
        <RouterLink to="/register">Register</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
    </nav>
</template>
  

<script setup lang="ts">
  import { RouterLink } from 'vue-router'
  import { isUserLoggedIn } from '@/stores/auth';
</script>


<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

nav {
  width: 100%;
  font-size: 18px;
  text-align: center;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}
</style>