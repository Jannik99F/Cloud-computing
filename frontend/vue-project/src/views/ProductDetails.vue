<template>
    <!-- If product couldn't be retrieved -->
    <div v-if="(product instanceof Error)">
        <p>{{ product.message }}</p>
        <p>Test</p>
    </div>

    <div v-else-if="product && !(product instanceof Error) 
                 && variances && !(variances instanceof Error)
                 && inventory && !(inventory instanceof Error)" 
                 class="product-box">
        <h1 class="product-header">{{ product.name }}</h1>
        <p>{{ product.product_type }}</p>
        <p>{{ product.height }}x{{ product.width }}x{{ product.depth }}cm</p>
        <div id="product-image">
            <!-- 
                TODO
                Put product images between product details and variances
            -->
        </div>
        <div class="variance-box">
            <div v-for="variance in variances" :key="variance.id" class="variance-item">
                <br>
                <div :style="{ backgroundColor: variance.name }"></div>
                <p>{{ variance.name }}</p>
                <p>{{ formatPrice(variance.price*product.base_price) }}</p>
                <p>Amount available: {{ getAmount(variance.id) }}</p>
            </div>
        </div>
    </div>
</template>

<script setup lang="ts">

    import type { Product } from '@/models/Product.vue';
    import { formatPrice } from '@/models/Product.vue';
    import type { Variance } from '@/models/Variance.vue';
    import type { Inventory } from '@/models/Inventory.vue';
    import { onMounted, ref } from 'vue';
    import { useRoute } from 'vue-router';

    const product = ref<Product | Error>()
    const variances = ref<Variance[] | Error>()
    const inventory = ref<Inventory[] | Error>()

    onMounted(() => {
        console.log('Product details page mounted')

        const route = useRoute()
        getProduct(route.params.id.toString()) // Init the product ref
        getVariances(route.params.id.toString()) // Init the variances ref
        getInventory() // Init the inventory ref
    })

    const getAmount = (variance_id: number) => {
        if(inventory.value instanceof Error || inventory.value == undefined) return 0;
        for(const item of inventory.value) {
            if(item.variance_id == variance_id) {
                return item.amount
            }
        }
    }

    /**
     *  API calls
     */

    const getProduct = async (id: string) => {
        try {
            const response = await fetch(`http://localhost:8000/products/${id}`)
            product.value = await response.json()
        } catch (error) {
            console.error('Error fetching product with id ' + id, error)
            product.value = new Error('Error fetching product')
        }
    }

    const getVariances = async(id: string) => {
        try {
            const response = await fetch(`http://localhost:8000/products/${id}/variances`)
            variances.value = await response.json()
        } catch (error) {
            console.error('Error fetching variances for product with id ' + id, error)
            variances.value = new Error('Error fetching variances')
        }
    }

    const getInventory = async() => {
        if(variances.value instanceof Error || variances.value == undefined)
            console.log(variances.value);
        try {
            const response = await fetch(`http://localhost:8000/inventory/${variance_id}`)
            inventory.value = await response.json()
        } catch (error) {
            console.error('Error fetching inventory for variance with id ' + variance_id, error)
            inventory.value = new Error('Error fetching inventory')
        }
    }
</script>

<style scoped>
    .product-box {
        padding: 1rem;
    }
    .product-box p {
        font-size: large;
    }

    .product-header {
        color: white;
    }

    .variance-box {
        display: flex;
        gap: 1em;
    }

    .variance-item {
        display: flex;
        flex-direction: column;
        align-items: center;
        padding: 10px;
        gap: 5px;
    }

    .variance-item div {
        width: 36px;
        height: 36px;
        background-color: #ddd;
        border: 2px solid #aaa;
        border-radius: 30%;
    }

    .variance-item p {
        font-size: medium;
    }

</style>