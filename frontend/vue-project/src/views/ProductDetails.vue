<template v-if="ready">
    <div id="product-details" v-if="ready">
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
                    <p>{{ JSON.stringify(variance) }}</p>
                    <br>
                    <div :style="{ backgroundColor: variance.name }"></div>
                    <p>{{ variance.name }}</p>
                    <p>{{ formatPrice(variance.price*product.base_price) }}</p>
                    <p>Amount available: {{ getAmount(variance.id) }}</p>
                </div>
            </div>
        </div>
    </div>

    <p v-else>Loading...</p>
</template>

<script setup lang="ts">

    import type { Product } from '@/models/Product.vue';
    import { formatPrice } from '@/models/Product.vue';
    import type { Variance } from '@/models/Variance.vue';
    import type { Inventory } from '@/models/Inventory.vue';
    import { onMounted, ref, toRaw } from 'vue';
    import { useRoute } from 'vue-router';

    const ready = ref(false) // Only show template when ready is true

    const product = ref<Product>()
    const variances = ref<Variance[]>()
    const inventory = ref<Inventory[]>()

    const API_HOST = import.meta.env.VITE_API_URL || 'http:://localhost:8000'

    onMounted(async () => {
        console.log('Product details page mounted')

        const route = useRoute()

        await getProduct(route.params.id.toString()) // Init the product ref
        await getVariances(route.params.id.toString()) // Init the variances ref
        await getInventory() // Init the inventory ref

        ready.value = true;
    })

    const getAmount = (variance_id: number) => {
        console.log("Getting inventory for variance with id ", variance_id)

        if(inventory.value == undefined) {
            console.log("inventory undefined")
            return 0;
        }

        for(const item of inventory.value) {
            console.log("Checking item: ", item)
            const rawItem = toRaw(item)
            console.log("Raw item: ", rawItem)
            console.log("Item id: ", rawItem.id)
            if(item.variance_id == variance_id) {
                return rawItem.amount
            }
            return 0;
        }

        inventory.value.forEach((item) => {
            
        })
    }

    /**
     *  API calls
     */

    const getProduct = async (id: string) => {
        try {
            const response = await fetch(`${API_HOST}/products/${id}`)
            product.value = await response.json()
        } catch (error) {
            console.error('Error fetching product with id ' + id, error)
        }
    }

    const getVariances = async (id: string) => {
        try {
            const response = await fetch(`${API_HOST}/${id}/variances`)
            variances.value = await response.json()
        } catch (error) {
            console.error('Error fetching variances for product with id ' + id, error)
        }
    }

    const getInventory = async () => {
        let jsonResponses = [];

        if(variances.value == undefined) {
            console.log("Variances are not defined");
            return
        }

        for(const variance of variances.value) {
            try {
                const response = await fetch(`${API_HOST}/inventory/${variance.id}`)
                jsonResponses.push(await response.json())
            } catch (error) {
                console.error('Error fetching inventory for variance with id ' + variance.id, error)
            }
        }

        inventory.value = jsonResponses;
        console.log("Inventory: ", inventory.value)
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