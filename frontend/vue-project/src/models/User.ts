import type { Basket } from "./Basket"

export interface User {
    id: number
    first_name: string
    last_name: string
    email: string
    password: string
    address: string
    baskets: Basket[]
}