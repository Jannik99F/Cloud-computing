<template>
  <div class="product-details" v-if="product">
    <h1>{{ product.name }}</h1>
    <div class="product-info">
      <p class="furniture-type">{{ product.furniture_type }}</p>
      <p class="product-type">{{ product.product_type }}</p>
      <p class="price">{{ formatPrice(product.base_price) }}</p>
      <div class="dimensions">
        <h3>Dimensions:</h3>
        <p>Height: {{ product.height }} cm</p>
        <p>Width: {{ product.width }} cm</p>
        <p>Depth: {{ product.depth }} cm</p>
      </div>
    </div>
  </div>
  <div v-else>
    <p>Loading product details...</p>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import type { Product } from '../views/ProductCatalog.vue'

const route = useRoute()
const product = ref<Product | null>(null)
const API_HOST = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const fetchProduct = async () => {
  try {
    const productId = route.params.id
    const response = await fetch(`${API_HOST}/products/${productId}`)
    product.value = await response.json()
  } catch (error) {
    console.error('Error fetching product:', error)
  }
}

function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`
}

onMounted(() => {
  fetchProduct()
})
</script>

<style scoped>
.product-details {
  padding: 2rem;
  max-width: 800px;
  margin: 0 auto;
}

.product-info {
  margin-top: 2rem;
}

.furniture-type {
  color: #666;
  font-style: italic;
}

.product-type {
  margin: 1rem 0;
}

.price {
  font-size: 1.5rem;
  font-weight: bold;
  color: #333;
  margin: 1rem 0;
}

.dimensions {
  margin-top: 2rem;
  padding: 1rem;
  background-color: #f5f5f5;
  border-radius: 4px;
}

.dimensions h3 {
  margin-bottom: 1rem;
}
</style>
