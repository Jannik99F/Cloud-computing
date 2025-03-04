<template>
    <h1>Your Basket</h1>
    <div v-if="basket != undefined"> 
        <div :key="key" v-for="item of superBasket" class="basket-item">
            <div class="item-picture" style="border: none">
                <!-- Put thumbnail of the picture here -->
            </div>
            <div>
                <b>{{ item.product_name }}</b>
                <p>in</p>
                <p :style="{color: item.variance_name}">{{ item.variance_name }}</p>
            </div>
            <div>
                <b>Dimensions:</b>
                <p>{{ item.height }}x{{ item.height }}x{{ item.height }}cm</p>
            </div>
            <div style="border: none">
                <b>Price:</b>
                <p v-if="!(item.base_price == null) && !(item.variance_price == null)">{{formatPrice(item.base_price*item.variance_price)}}</p>
                <p v-else>Price not available</p>
            </div>
            <button class="button" style="background-color: red; transparent: 60%" @click="removeItem(item.basket_item_id, basket.user_id)">
                Remove Item
            </button>
        </div>
        <div style="text-align: right">
            <h2>Total price: {{ formatPrice(getPriceOfBasket()) }}</h2>
        </div>
        <button class="button" @click="checkout()">
            Checkout
        </button>
    </div>
    <div v-else>
        Basket could not be retrieved. Please try again.
    </div>
</template>

<script setup lang="ts">
    import type { Basket } from '@/models/Basket';
    import type { Variance } from '@/models/Variance';
    import { useAuthStore } from '@/stores/auth';
    import { getCurrentInstance, nextTick, onMounted, ref } from 'vue';
    import { formatPrice, type Product } from '@/models/Product';
    import { useRouter } from 'vue-router';

    const auth = useAuthStore()
    const router = useRouter()

    const key = ref(0);

    const basket = ref<Basket>()
    const variances = ref<Variance[]>()
    const products = ref<Product[]>([])
    const variancesInBasket = ref<Variance[]>()
    const superBasket = ref<SuperBasketItem[]>([])

    interface SuperBasketItem {
        // Base properties from basket item
        basket_item_id: number
        basket_id: number
        base_price: number | null
        variance_id: number
        amount: number
        variance_price: number | null

        // Properties from Variance
        variance_name: string
        variance_type: string
        product_id: number

        // Properties from Product
        product_name: string
        furniture_type: string
        product_type: string
        height: number
        width: number
        depth: number
    }

    onMounted(async () => {
        console.log("Basket page mounted")

        fetchMethods()
    })

    const fetchMethods = async () => {
        await getBasket()
        await fetchProducts()
        await fetchVariances()
        await getVariances()
        await constructSuperBasket()
    }

    const forceRerender = () => {
        fetchMethods()
        key.value += 1
    }

    const removeItem = async (basket_item_id: number, user_id: number) => {

        try {
            const response = await fetch(import.meta.env.VITE_API_URL + "/current-basket/remove-item/" + basket_item_id + "?user_id=" + user_id, {method: "DELETE", headers: {Accept: "*/*"}})
            console.log(await response.json())
        } catch (error) {
            console.error("Item could not be removed.", error)
        }

        console.log("Hello")
        forceRerender()
    }

    const checkout = () => {
        router.push("/catalog");
    }

    const getPriceOfBasket = () => {
        let totalPrice = 0
        
        if (basket.value?.basket_items == undefined) return totalPrice

        for (const item of basket.value.basket_items) {
            if(item.base_price == null || item.variance_price == null) return totalPrice
            totalPrice += item.base_price*item.variance_price
        }

        return totalPrice
    }

    // Inits the super basket array, where all basket items are stored with additional variance and product information
    const constructSuperBasket = async () => {
        const superBasketItem = ref<SuperBasketItem>({
            basket_item_id: 0,
            basket_id: 0,
            base_price: 0,
            variance_id: 0,
            amount: 0,
            variance_price: 0,
            variance_name: "init",
            variance_type: "init",
            product_id: 0,
            product_name: "init",
            furniture_type: "init",
            product_type: "init",
            height: 0,
            width: 0,
            depth: 0
        })

        if (basket.value?.basket_items == undefined || variancesInBasket.value == undefined || products.value == undefined) return;

        for (const item of basket.value.basket_items) {
            // Fill with base props
            superBasketItem.value.basket_item_id = item.id
            superBasketItem.value.basket_id = item.basket_id
            superBasketItem.value.base_price = item.base_price
            superBasketItem.value.variance_id = item.variance_id
            superBasketItem.value.amount = item.amount
            superBasketItem.value.variance_price = item.variance_price

            // Fill with variance props
            for (const variance of variancesInBasket.value) {
                if (item.variance_id == variance.id) {
                    superBasketItem.value.variance_name = variance.name
                    superBasketItem.value.variance_type = variance.variance_type
                    superBasketItem.value.product_id = variance.product_id
                }
            }

            // Fill with product props
            for (const product of products.value) {
                if (superBasketItem.value.product_id == product.id) {
                    superBasketItem.value.product_name = product.name
                    superBasketItem.value.furniture_type = product.furniture_type
                    superBasketItem.value.product_type = product.product_type
                    superBasketItem.value.height = product.height
                    superBasketItem.value.width = product.width
                    superBasketItem.value.depth = product.depth
                }
            }

            superBasket.value.push(superBasketItem.value)
        }

        console.log("Current super basket: ", superBasket.value)
    }

    const fetchVariances = async () => {
        let varianceArray = []
        for (const product of products.value) {
            if (product.variances) {
                for (const variance of product.variances) {
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

        console.log("Got basket: " + JSON.stringify(basket.value))
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

        for(const item of basket.value.basket_items) {
            for(const variance of variances.value) {
                if (item.variance_id == variance.id) variancesArray.push(variance)
            }
        }

        variancesInBasket.value = variancesArray
    }
</script>

<style scoped>
    h1 {
        margin-bottom: 50px;
        align-self: center
    }

    .basket {
        display: flex;
        flex-direction: column;         
    }

    .basket-item {
        display: flex;
        flex-direction: row;
        padding-bottom: 20px;
        gap: 0.4em;
        padding-top: 20px;
        border-bottom: 0.1px solid silver;
        border-top: 0.1px solid silver;
        font-size: 20px;
        width: max-content;
    }
    .basket-item div {
        display: flex;
        flex-direction: row;
        gap: 0.4em;
        border-right: 0.1px solid silver;
        padding-right: 20px;
        padding-left: 20px;
    }

    .button {
        display: flex;
        justify-content: flex-end;
        margin-left: auto;
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
    .checkout-button:hover {
        transform: scale(1.05);
    }
</style>
