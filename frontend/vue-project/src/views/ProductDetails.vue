<template>
    <div class="product-box">
        <h1 class="product-header"></h1>
    </div>
    <p>Test page for product id {{ $route.params.id }}</p>
</template>

<script setup lang="ts">
    import type { Product } from '@/models/Product.vue';

    const getProduct = async (id: number) => {
        let product;

        try {
            product = await fetch(`http://localhost:8000/products/${id}`)
        } catch (error) {
            console.error('Error fetching product with id ' + id, error)
        }
        
        return product;
    }
</script>

<style scoped>
    .product-box {
        padding: 1rem;
        background-color: red;
    }

    .product-header {
        color: white;
    }

</style>