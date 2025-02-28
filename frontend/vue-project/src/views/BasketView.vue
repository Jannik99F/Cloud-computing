<template>
    <h2>Your Basket</h2>
    
    <div class="basket">
        <div v-if="basket != undefined" v-for="variance of variancesInBasket" class="basket-item">
            <div>
                <!-- Put thumbnail of the picture here -->
            </div>
            <p>{{ variance.name }}</p>
        </div>
        <div v-else>
            Basket could not be retrieved. Please try again.
        </div>
    </div>
</template>

<script setup lang="ts">
    import type { Basket } from '@/models/Basket';
    import type { Variance } from '@/models/Variance';
    import { useAuthStore } from '@/stores/auth';
    import { onMounted, ref } from 'vue';
    import type { Product } from '@/models/Product';

    const auth = useAuthStore()

    const basket = ref<Basket>()
    const variances = ref<Variance[]>()
    const products = ref<Product[]>([])
    const variancesInBasket = ref<Variance[]>()

    onMounted(async () => {
        console.log("Basket page mounted")

        await getBasket()
        await fetchProducts()
        await fetchVariances()
        await getVariances()
    })

    const fetchVariances = async () => {
        let varianceArray = []
        for (const product of products.value) {
            if (product.variances) {
                for (const variance of product.variances) {
                    console.log("Variance: " + JSON.stringify(variance))
                    varianceArray.push(variance)
                }
            }
        }

        variances.value = varianceArray
    }

    const fetchProducts = async () => {
        try {
            const response = await fetch(`${import.meta.env.VITE_API_URL}/products`)
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

    const getBasket = async () => {
        if (!auth.user) {
            return
        }

        try {
            const requestOptions = {
                method: "PUT",
                headers: {
                    "Accept": "*/*"
                }
            }
            const basketResponse = await fetch(`${import.meta.env.VITE_API_URL}/current-basket?user_id=${auth.user.id}`, requestOptions)
            basket.value = await basketResponse.json()
        } catch (error) {
            console.error("Basket could not be retrieved.", error)   
        }
    }

    const getVariances = async () => {
        let variancesArray = []

        if(basket.value == undefined) {
            console.error("Basket is undefined")
            return
        } else if(basket.value.basket_items == undefined) {
            console.error("Basket is empty")
            return
        } else if(variances.value == undefined) {
            console.error("Variances undefined")
            return
        }

        console.log("Basket: " + JSON.stringify(basket.value))

        for(const item of basket.value.basket_items) {
            for(const variance of variances.value) {
                if (item.variance_id == variance.id) variancesArray.push(variance)
            }
        }

        variancesInBasket.value = variancesArray
    }
</script>

<style scoped>
    .basket {
        display: flex;
        flex-direction: column;         
    }

    .basket-item {
        display: flex;
        flex-direction: row;
    }
</style>
