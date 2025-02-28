import type { BasketItem } from "./BasketItem.ts"

export interface Basket {
    id: number
    user_id: number
    basket_items?: BasketItem[]
}