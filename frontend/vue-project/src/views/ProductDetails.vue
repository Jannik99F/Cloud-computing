<template>
    <p>Test page for product id {{ $route.params.id }}</p>

    <div v-if="(product instanceof Error)">
        <p>{{ product.message }}</p>
    </div>

    <div v-else-if="product && !(product instanceof Error)" class="product-box">
        <h1 class="product-header">{{ product.name }}</h1>
    </div>
</template>

<script setup lang="ts">

    import type { Product } from '@/models/Product.vue';
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';

    const product = ref<Product | Error>()

    const getProduct = async (id: string) => {
        try {
            const response = await fetch(`http://localhost:8000/products/${id}`)
            product.value = await response.json()
        } catch (error) {
            console.error('Error fetching product with id ' + id, error)
            product.value = new Error('Error fetching product')
        }
    }

    onMounted(() => {
        console.log('Product details page mounted')

        const route = useRoute()
        getProduct(route.params.id.toString()) // Init the product ref
    })
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