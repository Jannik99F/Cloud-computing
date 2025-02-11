<template>
    <p>Test page for product id</p>
</template>

<script setup lang="ts">
    import type { Product } from './ProductCatalog.vue';
    import { ref } from 'vue';

    function getProduct(id: number): Product {
        let product = ref<Product>({
            id: id,
            name: 'Leather Sectional Sofa',
            description: 'Modern L-shaped sectional sofa in genuine leather, perfect for large living rooms. Features adjustable headrests and storage compartment.',
            price: 1299.99,
            category: 'Living Room',
            image: '/api/placeholder/150/150'
        });

        return product;
    }
</script>