<template>
    <BaseAdmin>
        <div class="page-header">
            <h1>Mis Audios 🎧</h1>
            <button class="upload-button" @click="showModal = true">
                + Cargar Nuevo Audio
            </button>
        </div>

        <!-- Grid de audios -->
        <div class="audio-grid">
            <div v-for="audio in audios" :key="audio.id" class="audio-card">
                <div>
                    <div class="card-icon">🎵</div>
                    <div class="card-content">
                        <h3 class="card-title">{{ audio.title }}</h3>
                        <p class="card-date">
                            <span>Programado para:</span>
                            {{ formatDate(audio.play_date) }}
                        </p>
                    </div>
                </div>

                <div class="card-actions">
                    <button class="action-button edit-button">Editar</button>
                    <button class="action-button delete-button" @click="deleteAudio(audio.id)">
                        Eliminar
                    </button>
                </div>

                <!-- Botón play/pause dinámico -->
                <button class="play-button" @click="togglePlay(audio)">
                    {{ currentAudioId === audio.id && isPlaying ? '⏸' : '▶' }}
                </button>
            </div>
        </div>

        <!-- Modal para crear audio -->
        <CrearAudio v-if="showModal" @close="showModal = false" @saved="handleSaved" />
    </BaseAdmin>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import BaseAdmin from './BaseAdmin.vue';
import CrearAudio from './CrearAudio.vue';
import api from '../axios/axios';
import axios from 'axios';

const audios = ref([]);
const audioPlayer = ref(null);
const currentAudioId = ref(null);
const isPlaying = ref(false);
const showModal = ref(false);

// 🔹 Función para actualizar el estado de aviso en la API
const setAvisoActivo = async (activo, audioId = null, audioFile = null) => {
    try {
        const payload = { 
            activo: activo,
            audio_file: audioFile // URL completa del audio
        };
        
        if (activo && audioId) {
            payload.audio_id = audioId;
        }

        await axios.put('https://api.kyeroradio.com/api2/aviso/2/', payload);

    } catch (error) {
        // Error actualizando aviso
    }
};

// 🔹 Función para reproducir audio
const playAudio = async (audio) => {
    // Detener audio previo si hay uno
    if (audioPlayer.value && currentAudioId.value) {
        audioPlayer.value.pause();
        audioPlayer.value.currentTime = 0;
        await setAvisoActivo(false);
    }

    // Construir URL completa del archivo de audio
    const audioFileUrl = audio.file.startsWith('http') 
        ? audio.file 
        : `http://localhost:8000${audio.file}`;

    // Activar el aviso en el backend PRIMERO
    await setAvisoActivo(true, audio.id, audioFileUrl);

    // Crear y reproducir el nuevo audio (solo para previsualización en panel)
    audioPlayer.value = new Audio(audioFileUrl);
    currentAudioId.value = audio.id;
    isPlaying.value = true;

    try {
        await audioPlayer.value.play();
        
        // Cuando termina la canción automáticamente
        audioPlayer.value.onended = async () => {
            await stopAudio();
        };

        // Manejar errores de reproducción
        audioPlayer.value.onerror = async () => {
            await stopAudio();
        };

    } catch (err) {
        await stopAudio();
    }
};

// 🔹 Función para detener audio
const stopAudio = async () => {
    if (audioPlayer.value) {
        audioPlayer.value.pause();
        audioPlayer.value.currentTime = 0;
    }
    
    isPlaying.value = false;
    currentAudioId.value = null;
    
    // Desactivar el aviso en el backend
    await setAvisoActivo(false);
};

// 🔹 Alternar reproducción manual
const togglePlay = async (audio) => {
    // Si es el mismo audio y está reproduciendo, pausar
    if (currentAudioId.value === audio.id && isPlaying.value) {
        await stopAudio();
    } 
    // Si es otro audio o no está reproduciendo, reproducir
    else {
        await playAudio(audio);
    }
};

// 🔹 Traer audios
const fetchAudios = async () => {
    try {
        const response = await api.get('audios/');
        audios.value = response.data;
    } catch (error) {
        // Error cargando audios
    }
};

// 🔹 Eliminar audio
const deleteAudio = async (id) => {
    if (confirm("¿Estás seguro de eliminar este audio?")) {
        try {
            // Si el audio que se elimina está reproduciéndose, detenerlo
            if (currentAudioId.value === id && isPlaying.value) {
                await stopAudio();
            }
            
            await api.delete(`audios/${id}/`);
            audios.value = audios.value.filter(a => a.id !== id);
        } catch (error) {
            // Error al eliminar audio
        }
    }
};

// 🔹 Refrescar lista después de guardar en modal
const handleSaved = () => {
    fetchAudios();
    showModal.value = false;
};

// 🔹 Formatear fecha
const formatDate = (dateStr) => {
    const date = new Date(dateStr);
    return date.toLocaleString("es-ES", {
        day: "2-digit",
        month: "short",
        year: "numeric",
        hour: "numeric",
        minute: "2-digit",
        hour12: true,
    });
};

// 🔹 Verificar si hay audio programado (para reproducción automática por hora)
const checkScheduledAudios = () => {
    const now = new Date();
    
    audios.value.forEach(audio => {
        const scheduledTime = new Date(audio.play_date);
        
        // Si es la hora programada y no está reproduciéndose
        if (Math.abs(scheduledTime - now) < 60000 && // dentro de 1 minuto
            currentAudioId.value !== audio.id) {
            playAudio(audio);
        }
    });
};

onMounted(() => {
    fetchAudios();
    
    // Verificar audios programados cada 30 segundos
    setInterval(checkScheduledAudios, 30000);
});
</script>

<style scoped>
.page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;
}

.page-header h1 {
    font-size: 2rem;
    color: #333;
}

.upload-button {
    background-color: #03a9f4;
    color: white;
    border: none;
    border-radius: 50px;
    padding: 12px 24px;
    font-size: 1rem;
    font-weight: bold;
    cursor: pointer;
    transition: background-color 0.3s ease;
    box-shadow: 0 4px 10px rgba(3, 169, 244, 0.3);
}

.upload-button:hover {
    background-color: #0288d1;
}

.audio-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 25px;
}

.audio-card {
    background-color: #ffffff;
    border-radius: 16px;
    padding: 20px;
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
    position: relative;
    overflow: hidden;
    transition: transform 0.3s ease, box-shadow 0.3s ease;
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 180px;
}

.audio-card:hover {
    transform: translateY(-8px);
    box-shadow: 0 12px 30px rgba(0, 0, 0, 0.12);
}

.card-icon {
    font-size: 2.5rem;
    margin-bottom: 15px;
    opacity: 0.7;
}

.card-title {
    margin: 0 0 8px 0;
    font-size: 1.25rem;
    color: #2c3e50;
    font-weight: 600;
}

.card-date {
    margin: 0;
    font-size: 0.9rem;
    color: #7f8c8d;
    margin-bottom: 20px;
}

.card-date span {
    font-weight: 500;
    color: #95a5a6;
}

.card-actions {
    display: flex;
    gap: 10px;
    margin-top: auto;
}

.action-button {
    flex-grow: 1;
    padding: 8px 12px;
    border-radius: 8px;
    border: 1px solid #ddd;
    background-color: transparent;
    cursor: pointer;
    font-size: 0.9rem;
    font-weight: 500;
    transition: all 0.2s ease-in-out;
}

.edit-button {
    color: #3498db;
    border-color: #3498db;
}

.edit-button:hover {
    background-color: #3498db;
    color: white;
}

.delete-button {
    color: #e74c3c;
    border-color: #e74c3c;
}

.delete-button:hover {
    background-color: #e74c3c;
    color: white;
}

.play-button {
    width: 30px;
    height: 30px;
    background-color: #03a9f4;
    border-radius: 50%;
    border: none;
    color: white;
    font-size: 1.5rem;
    display: flex;
    justify-content: center;
    align-items: center;
    cursor: pointer;
    position: absolute;
    bottom: 20px;
    top: 20px;
    right: 20px;
    transition: transform 0.2s ease;
    box-shadow: 0 4px 10px rgba(3, 169, 244, 0.4);
}

.play-button:hover {
    transform: scale(1.1);
}
</style>