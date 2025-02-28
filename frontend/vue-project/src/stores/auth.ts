import type { User } from '@/models/User';
import { defineStore } from 'pinia';

export const useAuthStore = defineStore("auth", {
  state: () => ({
    user: null as null | User,
  }),
  actions: {
    login(user: User) {
      this.user = user;
    },
    logout() {
      this.user = null;
    },
  },
});

export const isUserLoggedIn = () => {
    const auth = useAuthStore();

    if(auth.user) {
        console.log(auth.user.first_name, " ", auth.user.last_name, " is logged in.")
        return true
    }

    console.log("No user logged in")
    return false
}