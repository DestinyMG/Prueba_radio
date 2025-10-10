// src/stores/auth.js
import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
    state: () => ({
        access: null,
        refresh: null,
    }),
    actions: {
        setTokens(tokens) {
            this.access = tokens.access
            this.refresh = tokens.refresh
            // Guardar en localStorage para persistencia
            localStorage.setItem('auth_tokens', JSON.stringify(tokens))
        },
        loadTokens() {
            const stored = localStorage.getItem('auth_tokens')
            if (stored) {
                const tokens = JSON.parse(stored)
                this.access = tokens.access
                this.refresh = tokens.refresh
            }
        },
        clearTokens() {
            this.access = null
            this.refresh = null
            localStorage.removeItem('auth_tokens')
        }
    }
})
