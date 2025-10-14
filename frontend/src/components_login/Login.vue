<template>
  <div class="login-wrapper">
    <div class="login-container">
      <div class="login-header">
        <div class="logo">
          <i class="fas fa-user-shield"></i>
        </div>
        <h2>Iniciar Sesión</h2>
        <p>Ingresa tus credenciales para acceder</p>
      </div>

      <form @submit.prevent="handleLogin" class="login-form">
        <div class="form-group">
          <label for="username">Usuario</label>
          <div class="input-container">
            <i class="fas fa-user input-icon"></i>
            <input 
              v-model="username" 
              type="text" 
              id="username" 
              maxlength="15" 
              required 
              @input="filterUsername"
              placeholder="Ingresa tu usuario"
            />
          </div>
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <div class="input-container">
            <i class="fas fa-lock input-icon"></i>
            <input 
              v-model="password" 
              :type="showPassword ? 'text' : 'password'" 
              id="password" 
              maxlength="12" 
              required
              @input="filterPassword"
              placeholder="Ingresa tu contraseña"
            />
            <button 
              type="button" 
              class="password-toggle"
              @click="showPassword = !showPassword"
            >
              <i :class="showPassword ? 'fas fa-eye-slash' : 'fas fa-eye'"></i>
            </button>
          </div>
        </div>

        <button type="submit" class="login-btn" :disabled="isLoading">
          <span v-if="!isLoading">Ingresar</span>
          <div v-else class="loading-spinner"></div>
        </button>

        <div v-if="errorMessage" class="error-message">
          <i class="fas fa-exclamation-circle"></i>
          {{ errorMessage }}
        </div>
      </form>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import { useRouter } from 'vue-router';
import { useAuthStore } from '../stores/auth';

const username = ref('');
const password = ref('');
const showPassword = ref(false);
const rememberMe = ref(false);
const isLoading = ref(false);
const errorMessage = ref('');

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
  if (!username.value || !password.value) {
    errorMessage.value = 'Por favor, completa todos los campos';
    return;
  }

  isLoading.value = true;
  errorMessage.value = '';

  try {
    const response = await axios.post('http://localhost:8000/api/login/token/', {
      username: username.value,
      password: password.value
    });

    // Guardar tokens en Pinia
    authStore.setTokens(response.data);

    // Redirigir a componente Audios
    router.push({ name: 'audios' });

  } catch (err) {
    console.error('Error de autenticación', err);
    errorMessage.value = 'Usuario o contraseña incorrectos';
  } finally {
    isLoading.value = false;
  }
};
</script>

<style scoped>
.login-wrapper {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #1466e1 0%, #0d4fb5 100%);
  padding: 20px;
}

.login-container {
  width: 100%;
  max-width: 420px;
  background: #fff;
  border-radius: 16px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
  padding: 40px 30px;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(30px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 70px;
  height: 70px;
  background: linear-gradient(135deg, #1466e1, #0d4fb5);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin: 0 auto 20px;
}

.logo i {
  font-size: 28px;
  color: white;
}

.login-header h2 {
  color: #1466e1;
  margin-bottom: 8px;
  font-size: 24px;
  font-weight: 600;
}

.login-header p {
  color: #666;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 24px;
}

label {
  display: block;
  margin-bottom: 8px;
  color: #333;
  font-weight: 500;
  font-size: 14px;
}

.input-container {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 15px;
  color: #1466e1;
  font-size: 16px;
  z-index: 1;
}

input {
  width: 100%;
  padding: 14px 14px 14px 45px;
  border: 2px solid #e1e5ee;
  border-radius: 10px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

input:focus {
  outline: none;
  border-color: #1466e1;
  background: white;
  box-shadow: 0 0 0 3px rgba(20, 102, 225, 0.1);
}

.password-toggle {
  position: absolute;
  right: 15px;
  background: none;
  border: none;
  color: #666;
  cursor: pointer;
  font-size: 16px;
  padding: 0;
}

.password-toggle:hover {
  color: #1466e1;
}

.char-counter {
  text-align: right;
  font-size: 12px;
  color: #999;
  margin-top: 4px;
}

.form-options {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 25px;
  font-size: 14px;
}

.remember-me {
  display: flex;
  align-items: center;
  cursor: pointer;
  color: #555;
}

.remember-me input {
  display: none;
}

.checkmark {
  width: 18px;
  height: 18px;
  border: 2px solid #ddd;
  border-radius: 4px;
  margin-right: 8px;
  position: relative;
  transition: all 0.3s ease;
}

.remember-me input:checked + .checkmark {
  background: #1466e1;
  border-color: #1466e1;
}

.remember-me input:checked + .checkmark::after {
  content: '✓';
  position: absolute;
  color: white;
  font-size: 12px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

.forgot-password {
  color: #1466e1;
  text-decoration: none;
  transition: color 0.3s ease;
}

.forgot-password:hover {
  color: #0d4fb5;
  text-decoration: underline;
}

.login-btn {
  width: 100%;
  padding: 15px;
  background: linear-gradient(135deg, #1466e1, #0d4fb5);
  color: white;
  border: none;
  border-radius: 10px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.login-btn:hover:not(:disabled) {
  transform: translateY(-2px);
  box-shadow: 0 5px 15px rgba(20, 102, 225, 0.4);
}

.login-btn:disabled {
  opacity: 0.7;
  cursor: not-allowed;
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 2px solid transparent;
  border-top: 2px solid white;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin: 0 auto;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-message {
  background: #fee;
  color: #d32f2f;
  padding: 12px;
  border-radius: 8px;
  margin-top: 15px;
  font-size: 14px;
  display: flex;
  align-items: center;
  border-left: 4px solid #d32f2f;
}

.error-message i {
  margin-right: 8px;
}

.login-footer {
  text-align: center;
  padding-top: 20px;
  border-top: 1px solid #eee;
  color: #666;
  font-size: 14px;
}

.login-footer a {
  color: #1466e1;
  text-decoration: none;
  font-weight: 500;
}

.login-footer a:hover {
  text-decoration: underline;
}

/* Responsive Design */
@media (max-width: 480px) {
  .login-container {
    padding: 30px 20px;
    margin: 10px;
  }

  .login-wrapper {
    padding: 10px;
    align-items: flex-start;
    padding-top: 40px;
  }

  .form-options {
    flex-direction: column;
    gap: 15px;
    align-items: flex-start;
  }

  .forgot-password {
    align-self: flex-end;
  }
}

@media (max-width: 360px) {
  .login-header h2 {
    font-size: 20px;
  }

  input {
    padding: 12px 12px 12px 40px;
  }

  .input-icon {
    left: 12px;
  }
}
</style>