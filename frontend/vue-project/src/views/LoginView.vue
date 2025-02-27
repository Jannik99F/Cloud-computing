<template>
    <div>
        <h2>Please enter your E-Mail address and password</h2>

        <Form @submit="login" class="login-form">
            <div>
                <label>E-Mail Address</label>
                <Field name="email" :rules="isEmpty" v-model="form.email" class="input" />
                <ErrorMessage name="email" class="error" />
            </div>

            <div>
                <label>Password</label>
                <Field name="password" :rules="isEmpty" v-model="form.password" class="input" />
                <ErrorMessage name="password" class="error" />
            </div>

            <button type="submit" class="login-button">Login</button>
        </Form>
    </div>
</template>

<script setup lang="ts">
    import type { User } from "@/models/User";
    import { useAuthStore } from "@/stores/auth";
    import { Field, ErrorMessage, Form } from "vee-validate";
    import { reactive, ref } from "vue";
    import { useRouter } from "vue-router";

    const auth = useAuthStore()
    const router = useRouter()
    const users = ref<User[]>()

    const form = reactive({
        email: "",
        password: ""
    })

    const login = async () => {
        // Fetch users from DB
        try {
            const response = await fetch(import.meta.env.VITE_API_URL + "/users")
            users.value = await response.json()
        } catch (error) {
            console.error("Users could not be retrieved.")
            return
        }

        // Users still undefined?
        if(users.value == undefined) return
        
        // Iterate through users and find matching mail and password
        let matchedUser = undefined;
        for(const user of users.value) {
            if (user.email == form.email && user.password == form.password) matchedUser = user;
        }

        // No user found: matchedUser stays undefined
        if (matchedUser == undefined) {
            alert("Login unsuccessful. Please try again.")
            return
        }
        
        // User was found: Login, alert and go back to home
        auth.login(matchedUser)
        alert("Login successful!")
        router.push("/")
    }

    const isEmpty = (value: unknown) => {
        if (!value) return "Please enter a value."
        return true;
    }
</script>

<style scoped>
    .login-form {
        display: flex;
        flex-direction: column;
        gap: 8px;
        margin-top: 8px;
    }
    .login-form div {
        display: flex;
        flex-direction: column;
        gap: 4px;
    }
    .login-form input {
        width: 50%;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }
    .login-form button {
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
    .login-form button:hover {
        transform: scale(1.05);
    }

    .error {
        color: red;
    }
</style>