<template>
    <div class="receiver">
        <h2>Audio en vivo HD</h2>
        <button @click="toggleListening" :disabled="isConnecting">
            {{ getButtonText }}
        </button>
        <div v-if="status" class="status" :class="statusClass">{{ status }}</div>
        <audio ref="audioEl" controls autoplay></audio>
    </div>
</template>

<script setup>
import { ref, onUnmounted, computed } from 'vue';

const audioEl = ref(null);
let ws = null;
let audioContext = null;
let audioQueue = [];
let isPlaying = false;
let lastPlayTime = 0;

const listening = ref(false);
const isConnecting = ref(false);
const status = ref('');

const statusClass = computed(() => {
    if (status.value.includes('Error')) return 'error';
    if (status.value.includes('Conectado')) return 'success';
    if (status.value.includes('Escuchando')) return 'success';
    return 'info';
});

const getButtonText = computed(() => {
    if (isConnecting.value) return 'Conectando...';
    return listening.value ? '🔴 Detener' : '🎧 Escuchar HD';
});

const toggleListening = () => {
    if (listening.value) {
        stopListening();
    } else {
        startListening();
    }
};

const startListening = () => {
    if (listening.value || isConnecting.value) return;

    isConnecting.value = true;
    status.value = 'Conectando...';
    audioQueue = [];

    connectWebSocket();
};

const connectWebSocket = () => {
    try {
        ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
        ws.binaryType = "arraybuffer";

        ws.onopen = () => {
            console.log('✅ WebSocket CONECTADO');
            listening.value = true;
            isConnecting.value = false;
            status.value = '✅ Conectado - Iniciando audio HD...';
            
            initializeAudioContext();
        };

        ws.onmessage = (event) => {
            if (!listening.value || !audioContext) return;

            if (event.data instanceof ArrayBuffer && event.data.byteLength > 0) {
                // Procesar inmediatamente
                processRawAudio(event.data);
            }
        };

        ws.onclose = (event) => {
            console.log('WebSocket cerrado');
            listening.value = false;
            isConnecting.value = false;
            
            if (event.code !== 1000) {
                status.value = 'Conexión perdida';
                setTimeout(() => {
                    if (!listening.value && !isConnecting.value) {
                        startListening();
                    }
                }, 3000);
            } else {
                status.value = 'Conexión cerrada';
            }
        };

        ws.onerror = (error) => {
            console.error('WebSocket error:', error);
            status.value = 'Error de conexión';
            listening.value = false;
            isConnecting.value = false;
        };

    } catch (error) {
        console.error('Error conectando WebSocket:', error);
        status.value = 'Error de conexión';
        isConnecting.value = false;
    }
};

const initializeAudioContext = () => {
    try {
        // AudioContext con alta calidad
        audioContext = new AudioContext({
            sampleRate: 48000 // ALTA CALIDAD
        });
        status.value = '🎧 Escuchando audio HD...';
        console.log('🔊 AudioContext HD listo');
    } catch (error) {
        console.error('Error inicializando audio:', error);
        status.value = 'Error en sistema de audio';
        stopListening();
    }
};

const processRawAudio = (rawData) => {
    if (!audioContext) return;

    try {
        // Convertir Int16 back to Float32
        const int16Data = new Int16Array(rawData);
        const float32Data = new Float32Array(int16Data.length);
        
        for (let i = 0; i < int16Data.length; i++) {
            float32Data[i] = int16Data[i] / (int16Data[i] < 0 ? 0x8000 : 0x7FFF);
        }

        // Aplicar filtro de suavizado para mejor calidad
        const smoothedData = smoothAudio(float32Data);

        // Crear buffer de audio
        const audioBuffer = audioContext.createBuffer(1, smoothedData.length, 48000);
        audioBuffer.getChannelData(0).set(smoothedData);

        // Controlar timing para evitar solapamiento
        const now = audioContext.currentTime;
        const playTime = Math.max(lastPlayTime, now);
        
        // Crear fuente y reproducir
        const source = audioContext.createBufferSource();
        source.buffer = audioBuffer;
        source.connect(audioContext.destination);
        source.start(playTime);
        
        lastPlayTime = playTime + audioBuffer.duration;

        if (!isPlaying) {
            isPlaying = true;
            console.log('🎵 Audio HD reproduciéndose!');
        }

    } catch (error) {
        console.log('Error procesando audio:', error);
    }
};

// Filtro de suavizado para mejor calidad
const smoothAudio = (input) => {
    const output = new Float32Array(input.length);
    
    // Filtro simple para reducir ruido
    for (let i = 0; i < input.length; i++) {
        if (i === 0 || i === input.length - 1) {
            output[i] = input[i];
        } else {
            // Promedio suavizado
            output[i] = (input[i-1] + input[i] + input[i+1]) / 3;
        }
    }
    
    return output;
};

const stopListening = () => {
    console.log('🛑 Deteniendo receptor...');
    listening.value = false;
    isConnecting.value = false;
    isPlaying = false;
    lastPlayTime = 0;
    
    if (ws) {
        ws.close(1000, "Usuario detuvo");
        ws = null;
    }
    
    audioQueue = [];
    
    if (audioContext) {
        audioContext.close();
        audioContext = null;
    }
    
    status.value = 'Detenido';
};

const cleanup = () => {
    stopListening();
};

onUnmounted(() => {
    cleanup();
});
</script>

<style scoped>
.receiver {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin: 20px;
    text-align: center;
    max-width: 500px;
    margin: 0 auto;
    padding: 20px;
}

audio {
    width: 100%;
    max-width: 400px;
    margin-top: 10px;
}

button {
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    background-color: #10b981;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    min-width: 140px;
}

button:hover:not(:disabled) {
    background-color: #059669;
    transform: translateY(-2px);
}

button:disabled {
    background-color: #6b7280;
    cursor: not-allowed;
    opacity: 0.7;
}

.status {
    padding: 8px 16px;
    border-radius: 6px;
    font-weight: 500;
    text-align: center;
    min-width: 250px;
}

.status.info {
    background-color: #dbeafe;
    color: #1e40af;
    border: 1px solid #93c5fd;
}

.status.success {
    background-color: #dcfce7;
    color: #166534;
    border: 1px solid #86efac;
}

.status.error {
    background-color: #fee2e2;
    color: #991b1b;
    border: 1px solid #fca5a5;
}

h2 {
    color: #1f2937;
    margin-bottom: 10px;
}
</style>