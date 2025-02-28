<template>
    <div>
        <h2>Please enter your info to create an account</h2>

        <Form @submit="register" class="register-form">
            <div>
                <label>First Name</label>
                <Field name="firstName" :rules="isEmpty" v-model="form.first_name" />
                <ErrorMessage name="firstName" class="error" />
            </div>

            <div>
                <label>Last Name</label>
                <Field name="lastName" :rules="isEmpty" v-model="form.last_name" />
                <ErrorMessage name="lastName" class="error" />
            </div>

            <div>
                <label>Email</label>
                <Field name="email" :rules="isEmpty" v-model="form.email" />
                <ErrorMessage name="email" class="error" />
            </div>

            <div>
                <label>Password</label>
                <Field name="password" :rules="isEmpty" type="password" v-model="form.password" />
                <ErrorMessage name="password" class="error" />
            </div>

            <div>
                <label>Address</label>
                <Field name="address" :rules="isEmpty" v-model="form.address" />
                <ErrorMessage name="address" class="error" />
            </div>

            <button type="submit">Register</button>
        </Form>
    </div>
</template>

<script setup lang="ts">

    import { reactive, ref } from "vue";
    import { useAuthStore } from "@/stores/auth";
    import { useRouter } from "vue-router";
    import { Field, ErrorMessage, Form } from "vee-validate";
    import type { User } from "@/models/User"

    const auth = useAuthStore()
    const router = useRouter()
    const user = ref<User>();

    const form = reactive({
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        address: "",
    })

    const register = async () => {
        // Create user in DB
        try {
            // Create request header and body
            const requestOptions = {
                method: "POST",
                headers: { "Content-Type": "application/json", "Accept": "*/*" },
                body: JSON.stringify(form)
            };
            
            // Call API
            const response = await fetch(import.meta.env.VITE_API_URL+"/users", requestOptions)
            user.value = await response.json()
            
            // Set user in pinia store
            if (user.value != undefined) {
                auth.login(user.value)
            }

            // Popup and redirect to home
            alert("Registration successful!")
            router.push("/")
        } catch (error) {
            console.error("Registration could not be completed.", error)
            return
        }
    }

    const isEmpty = (value: unknown) => {
        if (!value) return "Please enter a value."
        return true
    }
</script>

<style scoped>
    .register-form {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 8px;
    }
    .register-form div {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .register-form input {
        width: 50%;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .register-form button {
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
    .register-form button:hover {
        transform: scale(1.05);
    }

    .error {
        color: red;
    }
</style>
