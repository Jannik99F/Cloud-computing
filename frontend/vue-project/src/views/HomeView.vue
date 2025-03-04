<template>
  <div id="home" class="home">
    <div>
      <h1>Welcome to LowTech Furniture!</h1>
    </div>
    <div>
      <p>Browse our current products under Catalog</p>
    </div>
    <div>
      <p>Please note that purchases are only available with a user account. If you don't have an account yet, please register.</p>
    </div>
  </div>
</template>

<script setup lang="ts">

</script>

<style scoped>
  .home {
    display: flex;
    flex-direction: column;
    gap: 1.5em;
  }

  .home div {
    display: flex;
    flex-direction: row;
    gap: 0.4em;
  }

  p {
    font-size: 20px;
  }
</style>
