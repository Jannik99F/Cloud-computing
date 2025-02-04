<template>
  <div class="product-catalog">
    <h1>Product Catalog</h1>
    <div class="catalog-grid">
      <!-- Loop through products -->
      <div v-for="product in products" :key="product.id" class="product-card" @click="openProductDetails(product.id)">
        <img :src="product.image" :alt="product.name" class="product-image" />
        <h3>{{ product.name }}</h3>
        <p class="product-category">{{ product.category }}</p>
        <p class="product-description">{{ product.description }}</p>
        <p class="product-price">{{ formatPrice(product.price) }}</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

export interface Product {
  id: number
  name: string
  description: string
  price: number
  category: string
  image: string
}

const products = ref<Product[]>([
  {
    id: 1,
    name: 'Leather Sectional Sofa',
    description:
      'Modern L-shaped sectional sofa in genuine leather, perfect for large living rooms. Features adjustable headrests and storage compartment.',
    price: 1299.99,
    category: 'Living Room',
    image: '/api/placeholder/150/150',
  },
  {
    id: 2,
    name: 'Solid Oak Dining Table',
    description:
      'Handcrafted dining table made from solid oak with a natural finish. Seats 6-8 people comfortably.',
    price: 899.99,
    category: 'Dining Room',
    image: '/api/placeholder/150/150',
  },
  {
    id: 3,
    name: 'Queen Platform Bed',
    description:
      'Modern platform bed with integrated LED lighting and USB charging ports. Includes headboard.',
    price: 799.99,
    category: 'Bedroom',
    image: '/api/placeholder/150/150',
  },
  {
    id: 4,
    name: 'Ergonomic Office Chair',
    description:
      'Adjustable mesh office chair with lumbar support, swivel base, and breathable material.',
    price: 299.99,
    category: 'Office',
    image: '/api/placeholder/150/150',
  },
  {
    id: 5,
    name: 'Storage Ottoman',
    description:
      'Multi-functional ottoman with hidden storage space. Upholstered in premium linen fabric.',
    price: 149.99,
    category: 'Living Room',
    image: '/api/placeholder/150/150',
  },
  {
    id: 6,
    name: 'Bookshelf with Ladder',
    description:
      'Floor-to-ceiling bookshelf with sliding ladder. Features adjustable shelves and solid wood construction.',
    price: 899.99,
    category: 'Storage',
    image: '/api/placeholder/150/150',
  },
  {
    id: 7,
    name: 'Glass Console Table',
    description:
      'Modern glass and chrome console table with two tiers. Perfect for entryways or behind sofas.',
    price: 249.99,
    category: 'Living Room',
    image: '/api/placeholder/150/150',
  },
  {
    id: 8,
    name: 'Dresser with Mirror',
    description:
      '6-drawer dresser with attached mirror. Made from solid pine with smooth-gliding drawer tracks.',
    price: 599.99,
    category: 'Bedroom',
    image: '/api/placeholder/150/150',
  },
  {
    id: 9,
    name: 'Accent Armchair',
    description:
      'Mid-century modern armchair with tufted back. Upholstered in premium velvet fabric.',
    price: 449.99,
    category: 'Living Room',
    image: '/api/placeholder/150/150',
  },
  {
    id: 10,
    name: 'Kitchen Island Cart',
    description:
      'Mobile kitchen island with butcher block top, wine rack, and storage drawers. Includes locking wheels.',
    price: 379.99,
    category: 'Kitchen',
    image: '/api/placeholder/150/150',
  },
])
function formatPrice(price: number): string {
  return `$${price.toFixed(2)}`
}

function openProductDetails(id: number) {
  useRouter().push(`/${id}`);
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
