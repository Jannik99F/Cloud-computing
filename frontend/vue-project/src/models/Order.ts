export interface Order {
    id: number
    shipping_address: string | null
    billing_address: string | null
    payment_method: string | null
    payment_secret: string | null
    payed: boolean
    items_reserved: boolean
    status: string
    basket_id: number
}