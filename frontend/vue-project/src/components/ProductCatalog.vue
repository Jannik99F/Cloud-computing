<template>
  <div class="product-catalog">
    <h1>Product Catalog</h1>
    <div class="catalog-grid">
      <!-- Loop through products -->
      <div
        v-for="product in products"
        :key="product.id"
        class="product-card"
        @click="openProductDetails(product.id)"
      >
        <h3>{{ product.name }}</h3>
        <p class="product-category">{{ product.furniture_type }}</p>
        <p class="product-description">{{ product.product_type }}</p>
        <p class="product-price">{{ formatPrice(product.base_price) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'

export interface Product {
  id: number
  name: string
  base_price: number
  furniture_type: string
  product_type: string
  height: number
  width: number
  depth: number
  variances: any[]
}

const products = ref<Product[]>([])

const API_HOST = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const fetchProducts = async () => {
  try {
    const response = await fetch(`${API_HOST}/products`)
    if (response.ok) {
      const data = await response.json()
      products.value = data
      console.log('Successfully fetched products:', data)
    } else {
      console.error('Failed to fetch products, status:', response.status)
    }
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
  useRouter().push(`/${id}`)
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
