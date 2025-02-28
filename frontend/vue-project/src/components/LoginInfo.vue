<template>
    <p v-if="(isUserLoggedIn())">Logged in as {{ auth.user?.email }}</p>
    <p v-else>Not logged in. Please register or login to make a purchase.</p>
</template>

<script setup lang="ts">
import { isUserLoggedIn, useAuthStore } from '@/stores/auth';
const auth = useAuthStore()
</script>

<style scoped>
p {
  font-size: 18px;
}

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