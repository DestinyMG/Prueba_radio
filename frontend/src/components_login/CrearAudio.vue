<template>
    <div class="modal-overlay">
        <div class="modal">
            <h2 class="modal-title">🎶 Subir Nuevo Audio</h2>
            <form @submit.prevent="handleSubmit" class="modal-form">

                <!-- Campo título -->
                <div class="form-group">
                    <label for="title">Título</label>
                    <input v-model="title" type="text" id="title" placeholder="Ej: Podcast semanal" required />
                </div>

                <!-- Campo archivo -->
                <div class="form-group">
                    <label for="file">Archivo MP3</label>
                    <input type="file" id="file" @change="handleFileUpload" accept="audio/mp3" required />
                </div>

                <!-- Campo fecha -->
                <div class="form-group">
                    <label for="play_date">Fecha y Hora de reproducción</label>
                    <input v-model="playDate" type="datetime-local" id="play_date" required />
                </div>

                <!-- Botones -->
                <div class="modal-actions">
                    <button type="submit" class="btn btn-primary">✅ Enviar</button>
                    <button type="button" class="btn btn-secondary" @click="$emit('close')">❌ Cancelar</button>
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

const handleFileUpload = (e) => {
    file.value = e.target.files[0];
};

const handleSubmit = async () => {
    const formData = new FormData();
    formData.append('title', title.value);
    formData.append('file', file.value);
    formData.append('play_date', new Date(playDate.value).toISOString());

    // Obtener token del localStorage
    const tokens = localStorage.getItem('auth_tokens');
    const accessToken = tokens ? JSON.parse(tokens).access : null;

    if (!accessToken) {
        alert('No estás autenticado. Por favor, haz login.');
        return;
    }

    try {
        // Usamos api en lugar de axios, el token se añade automáticamente
        await api.post('audios/', formData, {
            headers: {
                'Content-Type': 'multipart/form-data'
            }
        });

        // Resetear y emitir eventos
        title.value = '';
        playDate.value = '';
        file.value = null;
        emit('saved');
        emit('close');
    } catch (err) {
        console.error('Error al subir audio:', err);
        alert('Ocurrió un error al subir el audio.');
    }
};
</script>


<style>
/* Fondo del modal */
.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(0, 0, 0, 0.7);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 999;
}

/* Contenedor modal */
.modal {
    background: #fff;
    padding: 2rem;
    border-radius: 16px;
    width: 420px;
    box-shadow: 0px 10px 30px rgba(0, 0, 0, 0.25);
    animation: fadeIn 0.3s ease-in-out;
}

/* Animación suave */
@keyframes fadeIn {
    from {
        opacity: 0;
        transform: translateY(-10px);
    }

    to {
        opacity: 1;
        transform: translateY(0);
    }
}

/* Título */
.modal-title {
    font-size: 1.5rem;
    font-weight: bold;
    margin-bottom: 1.5rem;
    text-align: center;
    color: #333;
}

/* Inputs */
.form-group {
    margin-bottom: 1.2rem;
    display: flex;
    flex-direction: column;
}

label {
    font-size: 0.95rem;
    font-weight: 600;
    margin-bottom: 0.4rem;
    color: #444;
}

input[type="text"],
input[type="datetime-local"],
input[type="file"] {
    padding: 0.7rem;
    border: 1px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    outline: none;
    transition: 0.2s;
}

input:focus {
    border-color: #007bff;
    box-shadow: 0 0 6px rgba(0, 123, 255, 0.3);
}

/* Botones */
.modal-actions {
    display: flex;
    justify-content: space-between;
    margin-top: 1.5rem;
}

.btn {
    padding: 0.7rem 1.2rem;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    font-size: 0.95rem;
    font-weight: 600;
    transition: background 0.2s ease-in-out;
}

.btn-primary {
    background: #007bff;
    color: white;
}

.btn-primary:hover {
    background: #0056b3;
}

.btn-secondary {
    background: #e0e0e0;
    color: #333;
}

.btn-secondary:hover {
    background: #cfcfcf;
}
</style>
