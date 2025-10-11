<template>
    <div class="login-container">
        <h2>Login</h2>
        <form @submit.prevent="handleLogin">
            <div class="form-group">
                <label for="username">Usuario</label>
                <input v-model="username" type="text" id="username" maxlength="15" required @input="filterUsername" />
            </div>

            <div class="form-group">
                <label for="password">Contraseña</label>
                <input v-model="password" type="password" id="password" maxlength="12" required
                    @input="filterPassword" />
            </div>

            <button type="submit">Ingresar</button>
        </form>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const username = ref('');
const password = ref('');

const router = useRouter();
const authStore = useAuthStore();

// 🔹 Filtros de entrada
const filterUsername = () => {
    username.value = username.value.replace(/[^a-zA-Z0-9]/g, '');
};

const filterPassword = () => {
    password.value = password.value.replace(/[^a-zA-Z0-9]/g, '');
};

const handleLogin = async () => {
    try {
        const response = await axios.post('https://prueba-radio.onrender.com/api/login/token/', {
            username: username.value,
            password: password.value
        });

        // Guardar tokens en Pinia
        authStore.setTokens(response.data);

        // Redirigir a componente Audios
        router.push({ name: 'audios' });

    } catch (err) {
        console.error('Usuario o contraseña incorrectos', err);
        alert('Usuario o contraseña incorrectos'); // opcional
    }
};
</script>



<style>
.login-container {
    width: 350px;
    margin: 3rem auto;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
    background: #fff;
}

.form-group {
    margin-bottom: 1rem;
}

label {
    display: block;
    margin-bottom: 0.25rem;
}

input {
    width: 100%;
    padding: 0.5rem;
    border-radius: 6px;
    border: 1px solid #ccc;
}

button {
    padding: 0.6rem 1.2rem;
    border: none;
    border-radius: 6px;
    background: #4CAF50;
    color: white;
    cursor: pointer;
}

button:hover {
    background: #45a049;
}

.error {
    color: red;
    margin-top: 1rem;
}

.success {
    color: green;
    margin-top: 1rem;
}
</style>
