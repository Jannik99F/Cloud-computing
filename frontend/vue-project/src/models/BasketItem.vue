<script lang="ts">

export interface BasketItem {
    id: number
    variance_id: number
    basket_id: number
    amount: number
    base_price: number | null
    variance_price: number | null
}

</script>