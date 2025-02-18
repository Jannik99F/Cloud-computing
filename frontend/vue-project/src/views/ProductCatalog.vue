<template>
  <div class="product-catalog">
    <h1>Product Catalog</h1>
    <div class="catalog-grid">
      <!-- Loop through products -->
      <div v-for="product in products" :key="product.id" class="product-card" @click="openProductDetails(product.id)">
        <h3>{{ product.name }}</h3>
        <p class="product-category">{{ product.furniture_type }}</p>
        <p class="product-description">{{ product.product_type }}</p>
        <p class="product-price">{{ formatPrice(product.base_price) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { Product } from '@/models/Product.vue';
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

const products = ref<Product[]>([])
const router = useRouter();

const fetchProducts = async () => {
  try {
    const response = await fetch('http://localhost:8000/products')
    products.value = await response.json()
  } catch (error) {
    console.error('Error fetching products:', error)
  }
}

onMounted(() => {
  fetchProducts()
})


function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`
}

function openProductDetails(id: number) {
  router.push(`/catalog/${id}`)
}
</script>

<style scoped>
.product-catalog {
  padding: 1rem;
}
.catalog-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
}
.product-card {
  border: 1px solid #ddd;
  border-radius: 4px;
  padding: 1rem;
  text-align: center;
}
.product-image {
  max-width: 100%;
  height: auto;
}
.product-category {
  font-style: italic;
  color: #777;
}
.product-description {
  margin: 0.5rem 0;
}
.product-price {
  font-weight: bold;
  color: #333;
}
</style>
