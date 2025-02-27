<template>

</template>

<script setup lang="ts">
    import { useAuthStore } from '@/stores/auth';
    import { onMounted } from 'vue';
    import { useRouter } from 'vue-router';

    const auth = useAuthStore()
    const router = useRouter()

    onMounted(async () => {        
        auth.logout()
        alert("Successfully logged out.")
        router.push("/login")
    })
</script>