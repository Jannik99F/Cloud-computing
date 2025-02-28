import type { Variance } from "./Variance"

export interface Product {
    id: number
    name: string
    base_price: number
    furniture_type: string
    product_type: string
    height: number
    width: number
    depth: number
    variances: Variance[]
}

export const formatPrice = (price: number): string => "$" + price.toFixed(2)