<template v-if="ready">
    <div id="product-details" v-if="ready">
        <!-- If product couldn't be retrieved -->
        <div v-if="product == undefined">
            <p>Could not retrieve product information.</p>
        </div>

        <div v-else>
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
                <div v-for="variance in variances" :key="variance.id" class="variance-item" :class="getVarianceItemStyleClass(variance.id)">
                    <div :style="{ backgroundColor: variance.name }"></div>
                    <p>{{ variance.name }}</p>
                    <p>{{ formatPrice(variance.price*product.base_price) }}</p>
                    <p>Amount available: {{ getAmount(variance.id) }}</p>
                    <button v-if="getAmount(variance.id) > 0" @click="addToBasket(variance.id)">Add to basket</button>
                    <button v-else>Not in stock</button>
                </div>
            </div>
        </div>
    </div>

    <p v-else>Loading...</p>
</template>

<script setup lang="ts">

    import type { Product } from '@/models/Product';
    import { formatPrice } from '@/models/Product';
    import type { Variance } from '@/models/Variance';
    import type { Inventory } from '@/models/Inventory';
    import { onMounted, ref } from 'vue';
    import { useRoute, useRouter } from 'vue-router';
    import { useAuthStore } from '@/stores/auth';

    const ready = ref(false) // Only show template when ready is true

    const product = ref<Product>()
    const variances = ref<Variance[]>()
    const inventory = ref<Inventory[]>()

    const auth = useAuthStore()
    const router = useRouter()

    // const API_HOST = "http://localhost:8000"
    const API_HOST = import.meta.env.VITE_API_URL || 'http://localhost:8000'

    onMounted(async () => {
        console.log('Product details page mounted')

        const route = useRoute()

        await getProduct(route.params.id.toString()) // Init the product ref
        await getVariances(route.params.id.toString()) // Init the variances ref
        await getInventory() // Init the inventory ref

        ready.value = true;
    })

    /**
     * Helper functions
     */

    const getAmount = (variance_id: number) => {
        let amount = 0

        if(inventory.value == undefined) {
            return 0
        }

        inventory.value.forEach((item) => {
            // Even if this is showing errors, this part is vital. 
            // Each item object is wrapped in an array of length one, 
            // so we need to access the first element to make it work.
            // @ts-ignore
            item = item['0']   // ?????????????? what the fuck vue ??????????????
            if(item.variance_id == variance_id) {
                amount = item.amount
            }
        });

        return amount
    }

    const getVarianceItemStyleClass = (variance_id: number) => {
        return getAmount(variance_id) > 0 
            ? 'available' 
            : 'unavailable'
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
            const response = await fetch(`${API_HOST}/products/${id}/variances`)
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
    }

    const addToBasket = async (variance_id: number) => {
        if (!auth.user) {
            alert("Please login or register to add items to your basket.")
            return
        }

        try {
            // Create request header and body
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json", "Accept": "*/*" },
                body: JSON.stringify({
                    "amount": 1,
                    "variance_id": variance_id
                })
            };

            const response = await fetch(import.meta.env.VITE_API_URL + "/current-basket/add-item?user_id=" + auth.user.id, requestOptions)
            if (response.ok) {
                const returnedBasket = await response.json()
                console.log("Current basket holds: ", returnedBasket)
                alert("Item was added to the basket!")
            } else if(response.status == 400) {
                alert("This item already exists in your basket.")
            }
        } catch (error) {
            console.error("Item could not be added to basket.", error)
            alert("There was a problem adding your item to the basket. Please try again.")
        }
    }
</script>

<style scoped>
    .product-header {
        color: var(--color-text)
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
        border: 2px solid #ddd;
        border-radius: 30%;
    }
    .available div {
        opacity: 90%;
    }
    .unavailable div {
        opacity: 15%;
    }
    .variance-item p {
        font-size: medium;
    }
    .available p {
        opacity: 90%
    }
    .unavailable p {
        opacity: 35%;
    }
    .variance-item button {
        background: transparent;
        border: 1px solid #ddd;
        border-radius: 8px;
        text-align: center;
        width: fit-content;
        margin-top: 8px;
        padding: 8px;
        font-size: 16px;
        color: var(--color-text);
    }
    .available button:hover {
        transform: scale(1.05);
    }
    .unavailable button {
        opacity: 35%;
    }
</style>
