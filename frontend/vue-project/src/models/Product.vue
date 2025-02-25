<script lang="ts">

export interface Product {
    id: number
    name: string
    base_price: number
    furniture_type: string
    product_type: string
    height: number
    width: number
    depth: number
    variances: any[]
}

export const formatPrice = (price: number): string => "$" + price.toFixed(2)
</script>