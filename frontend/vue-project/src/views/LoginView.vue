<template>
    <div>
        <h2>Login</h2>

        <Form @submit="login">
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

            <button type="submit">Login</button>
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
    .input {
        width: 100%;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .error {
        color: red;
    }
</style>