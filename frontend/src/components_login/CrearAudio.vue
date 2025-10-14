<template>
    <div class="modal-overlay">
        <div class="modal">
            <div class="modal-header">
                <h2 class="modal-title"><i class="fas fa-music"></i> Subir Nuevo Audio</h2>
                <button class="close-button" @click="$emit('close')" :disabled="isLoading">
                    <i class="fas fa-times"></i>
                </button>
            </div>
            
            <form @submit.prevent="handleSubmit" class="modal-form">
                <!-- Campo título -->
                <div class="form-group">
                    <label for="title">
                        <i class="fas fa-heading"></i> Título
                    </label>
                    <input v-model="title" type="text" id="title" placeholder="Ej: Podcast semanal" required 
                           :disabled="isLoading" />
                </div>

                <!-- Campo archivo -->
                <div class="form-group">
                    <label for="file">
                        <i class="fas fa-file-audio"></i> Archivo MP3
                    </label>
                    <div class="file-input-container">
                        <input type="file" id="file" @change="handleFileUpload" accept="audio/mp3" required 
                               :disabled="isLoading" />
                        <div class="file-input-custom" :class="{ 'disabled': isLoading }">
                            <i class="fas fa-upload"></i>
                            <span>{{ file ? file.name : 'Seleccionar archivo' }}</span>
                        </div>
                    </div>
                </div>

                <!-- Campo fecha -->
                <div class="form-group">
                    <label for="play_date">
                        <i class="fas fa-calendar-alt"></i> Fecha y Hora de reproducción
                    </label>
                    <input v-model="playDate" type="datetime-local" id="play_date" required 
                           :disabled="isLoading" />
                </div>

                <!-- Botones -->
                <div class="modal-actions">
                    <button type="submit" class="btn btn-primary" :disabled="isLoading">
                        <template v-if="isLoading">
                            <i class="fas fa-spinner fa-spin"></i> Subiendo...
                        </template>
                        <template v-else>
                            <i class="fas fa-check"></i> Subir Audio
                        </template>
                    </button>
                    <button type="button" class="btn btn-secondary" @click="$emit('close')" :disabled="isLoading">
                        <i class="fas fa-times"></i> Cancelar
                    </button>
                </div>
            </form>
        </div>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import axios from 'axios';
import api from '../axios/axios'

// Emitir eventos "saved" y "close"
const emit = defineEmits(['saved', 'close']);

const title = ref('');
const playDate = ref('');
const file = ref(null);
const isLoading = ref(false);

const handleFileUpload = (e) => {
    if (isLoading.value) return;
    file.value = e.target.files[0];
};

const handleSubmit = async () => {
    // Prevenir doble envío
    if (isLoading.value) return;
    
    // Validar campos
    if (!title.value || !file.value || !playDate.value) {
        alert('Por favor, completa todos los campos.');
        return;
    }

    isLoading.value = true;

    const formData = new FormData();
    formData.append('title', title.value);
    formData.append('file', file.value);
    formData.append('play_date', new Date(playDate.value).toISOString());

    // Obtener token del localStorage
    const tokens = localStorage.getItem('auth_tokens');
    const accessToken = tokens ? JSON.parse(tokens).access : null;

    if (!accessToken) {
        alert('No estás autenticado. Por favor, haz login.');
        isLoading.value = false;
        return;
    }

    try {
        // Usamos api en lugar de axios, el token se añade automáticamente
        await api.post('audios/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            },
            timeout: 30000 // 30 segundos timeout
        });

        // Resetear y emitir eventos
        title.value = '';
        playDate.value = '';
        file.value = null;
        emit('saved');
        emit('close');
        
    } catch (err) {
        console.error('Error al subir audio:', err);
        let errorMessage = 'Ocurrió un error al subir el audio.';
        
        if (err.response) {
            // Error del servidor
            if (err.response.status === 400) {
                errorMessage = 'Datos inválidos. Verifica el formato del archivo.';
            } else if (err.response.status === 413) {
                errorMessage = 'El archivo es demasiado grande.';
            } else if (err.response.status === 500) {
                errorMessage = 'Error del servidor. Intenta más tarde.';
            }
        } else if (err.request) {
            // Error de red
            errorMessage = 'Error de conexión. Verifica tu internet.';
        }
        
        alert(errorMessage);
    } finally {
        isLoading.value = false;
    }
};
</script>

<style scoped>
/* Fondo del modal - ARREGLADO */
.modal-overlay {
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    bottom: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 1000;
    padding: 20px;
    backdrop-filter: blur(5px);
    box-sizing: border-box;
}

/* Contenedor modal - ARREGLADO */
.modal {
    background: #fff;
    border-radius: 20px;
    max-width: min(480px, calc(100vw - 40px));
    width: 100%;
    box-shadow: 0 25px 60px rgba(0, 0, 0, 0.3);
    animation: modalSlideIn 0.3s ease-out;
    overflow: hidden;
    margin: 0 auto;
}

@keyframes modalSlideIn {
    from {
        opacity: 0;
        transform: translateY(-20px) scale(0.95);
    }
    to {
        opacity: 1;
        transform: translateY(0) scale(1);
    }
}

/* Header del modal */
.modal-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 25px 30px;
    border-bottom: 1px solid #f0f0f0;
    background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
}

.modal-title {
    font-size: 1.4rem;
    font-weight: 700;
    margin: 0;
    color: #2c3e50;
    display: flex;
    align-items: center;
    gap: 10px;
}

.close-button {
    background: none;
    border: none;
    font-size: 1.3rem;
    cursor: pointer;
    color: #7f8c8d;
    transition: all 0.3s ease;
    width: 40px;
    height: 40px;
    display: flex;
    align-items: center;
    justify-content: center;
    border-radius: 50%;
    flex-shrink: 0;
}

.close-button:hover:not(:disabled) {
    background: #f8f9fa;
    color: #e74c3c;
}

.close-button:disabled {
    opacity: 0.5;
    cursor: not-allowed;
}

/* Formulario */
.modal-form {
    padding: 25px 30px;
}

.form-group {
    margin-bottom: 20px;
}

label {
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 8px;
    color: #2c3e50;
}

label i {
    color: #03a9f4;
    width: 16px;
    flex-shrink: 0;
}

/* Inputs generales */
input[type="text"],
input[type="datetime-local"] {
    width: 100%;
    padding: 12px 16px;
    border: 2px solid #e9ecef;
    border-radius: 12px;
    font-size: 1rem;
    font-family: 'Montserrat', sans-serif;
    outline: none;
    transition: all 0.3s ease;
    background: #fff;
    box-sizing: border-box;
}

input[type="text"]:focus:not(:disabled),
input[type="datetime-local"]:focus:not(:disabled) {
    border-color: #03a9f4;
    box-shadow: 0 0 0 3px rgba(3, 169, 244, 0.1);
    transform: translateY(-1px);
}

input:disabled {
    background-color: #f8f9fa;
    color: #6c757d;
    cursor: not-allowed;
    opacity: 0.7;
}

/* File input personalizado */
.file-input-container {
    position: relative;
    width: 100%;
}

.file-input-container input[type="file"] {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
    z-index: 2;
}

.file-input-container input[type="file"]:disabled {
    cursor: not-allowed;
}

.file-input-custom {
    width: 100%;
    padding: 12px 16px;
    border: 2px dashed #e9ecef;
    border-radius: 12px;
    background: #f8f9fa;
    display: flex;
    align-items: center;
    gap: 10px;
    transition: all 0.3s ease;
    cursor: pointer;
    color: #6c757d;
    box-sizing: border-box;
    min-height: 48px;
}

.file-input-custom:hover:not(.disabled) {
    border-color: #03a9f4;
    background: #f1f9fe;
    color: #03a9f4;
}

.file-input-custom.disabled {
    background: #e9ecef;
    color: #adb5bd;
    cursor: not-allowed;
    border-color: #dee2e6;
}

.file-input-custom i {
    font-size: 1.1rem;
    flex-shrink: 0;
}

.file-input-custom span {
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
    flex: 1;
}

.file-input-container input[type="file"]:focus + .file-input-custom:not(.disabled) {
    border-color: #03a9f4;
    box-shadow: 0 0 0 3px rgba(3, 169, 244, 0.1);
}

/* Botones */
.modal-actions {
    display: flex;
    gap: 15px;
    margin-top: 25px;
}

.btn {
    flex: 1;
    padding: 12px 20px;
    border: none;
    border-radius: 12px;
    font-size: 1rem;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 8px;
    font-family: 'Montserrat', sans-serif;
    box-sizing: border-box;
    min-height: 48px;
    position: relative;
    overflow: hidden;
}

.btn-primary {
    background: linear-gradient(45deg, #03a9f4, #0288d1);
    color: white;
    box-shadow: 0 4px 15px rgba(3, 169, 244, 0.3);
}

.btn-primary:hover:not(:disabled) {
    background: linear-gradient(45deg, #0288d1, #0277bd);
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(3, 169, 244, 0.4);
}

.btn-primary:disabled {
    background: linear-gradient(45deg, #81d4fa, #4fc3f7);
    cursor: not-allowed;
    transform: none;
    box-shadow: 0 2px 8px rgba(3, 169, 244, 0.2);
}

.btn-secondary {
    background: #f8f9fa;
    color: #6c757d;
    border: 2px solid #e9ecef;
}

.btn-secondary:hover:not(:disabled) {
    background: #e9ecef;
    color: #495057;
    transform: translateY(-2px);
    border-color: #dee2e6;
}

.btn-secondary:disabled {
    background: #e9ecef;
    color: #adb5bd;
    cursor: not-allowed;
    transform: none;
    border-color: #dee2e6;
}

/* Animación de spinner */
.fa-spin {
    animation: fa-spin 1s infinite linear;
}

@keyframes fa-spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

/* Efecto de carga en el botón */
.btn:disabled::after {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    animation: loading 1.5s infinite;
}

@keyframes loading {
    0% { left: -100%; }
    100% { left: 100%; }
}

/* Responsive MEJORADO */
@media (max-width: 768px) {
    .modal-overlay {
        padding: 15px;
    }
    
    .modal {
        max-width: min(400px, calc(100vw - 30px));
    }
    
    .modal-header {
        padding: 20px 25px;
    }
    
    .modal-form {
        padding: 20px 25px;
    }
    
    .modal-title {
        font-size: 1.3rem;
    }
    
    .modal-actions {
        flex-direction: column;
        gap: 12px;
    }
    
    .btn {
        padding: 12px 16px;
    }
}

@media (max-width: 480px) {
    .modal-overlay {
        padding: 10px;
    }
    
    .modal {
        max-width: calc(100vw - 20px);
        border-radius: 16px;
    }
    
    .modal-header {
        padding: 15px 20px;
    }
    
    .modal-form {
        padding: 15px 20px;
    }
    
    input[type="text"],
    input[type="datetime-local"],
    .file-input-custom {
        padding: 10px 12px;
    }
    
    .form-group {
        margin-bottom: 18px;
    }
    
    .modal-actions {
        margin-top: 20px;
    }
}

/* Placeholder styling */
input::placeholder {
    color: #adb5bd;
    font-weight: 400;
}

/* Validación visual */
input:invalid:not(:disabled) {
    border-color: #e74c3c;
}

input:valid:not(:disabled) {
    border-color: #27ae60;
}

/* Asegurar que no haya scroll horizontal */
html, body {
    overflow-x: hidden;
}
</style>