<template>
    <div class="transmitter">
        <h2>Transmisor HD</h2>
        <button @click="toggleTransmit" :disabled="isConnecting">
            {{ transmitting ? '🔴 Detener' : '🎤 Transmitir HD' }}
        </button>
        <div v-if="status" class="status">{{ status }}</div>
    </div>
</template>

<script setup>
import { ref } from 'vue';

const transmitting = ref(false);
const isConnecting = ref(false);
const status = ref('');
let ws;
let audioContext;
let processor;
let stream;

const toggleTransmit = async () => {
    if (!transmitting.value) {
        await startTransmitting();
    } else {
        stopTransmitting();
    }
};

const startTransmitting = async () => {
    if (transmitting.value || isConnecting.value) return;

    isConnecting.value = true;
    status.value = 'Conectando...';

    try {
        // Conectar WebSocket
        ws = new WebSocket("wss://prueba-radio.onrender.com/ws/streaming/");
        ws.binaryType = "arraybuffer";

        await new Promise((resolve, reject) => {
            ws.onopen = resolve;
            ws.onerror = reject;
            setTimeout(() => reject(new Error('Timeout')), 5000);
        });

        status.value = 'Configurando audio HD...';

        // Obtener micrófono con ALTA CALIDAD
        stream = await navigator.mediaDevices.getUserMedia({ 
            audio: {
                channelCount: 1,
                sampleRate: 48000, // ALTA CALIDAD
                echoCancellation: true,
                noiseSuppression: true,
                autoGainControl: false // Mejor desactivar para calidad
            } 
        });

        // Crear AudioContext con alta calidad
        audioContext = new AudioContext({
            sampleRate: 48000 // ALTA CALIDAD
        });
        const source = audioContext.createMediaStreamSource(stream);

        // Buffer más grande para mejor calidad y menos latencia
        processor = audioContext.createScriptProcessor(2048, 1, 1);

        processor.onaudioprocess = (event) => {
            if (!transmitting.value || ws.readyState !== WebSocket.OPEN) return;

            // Obtener datos de audio
            const inputData = event.inputBuffer.getChannelData(0);
            
            // Comprimir ligeramente para mejorar claridad
            const processedData = compressAudio(inputData);
            
            // Convertir a Int16
            const int16Data = floatTo16BitPCM(processedData);
            
            // Enviar
            ws.send(int16Data);
        };

        // Conectar
        source.connect(processor);
        processor.connect(audioContext.destination);

        transmitting.value = true;
        isConnecting.value = false;
        status.value = '🎤 Transmitiendo audio HD...';

        console.log('🚀 Transmisión HD INICIADA');

    } catch (error) {
        console.error('Error:', error);
        status.value = `Error: ${error.message}`;
        stopTransmitting();
    }
};

// Compresión suave para mejorar claridad
const compressAudio = (input) => {
    const output = new Float32Array(input.length);
    const threshold = 0.5;
    const ratio = 1.5;
    
    for (let i = 0; i < input.length; i++) {
        let sample = input[i];
        
        // Compresión suave
        if (Math.abs(sample) > threshold) {
            sample = Math.sign(sample) * (threshold + (Math.abs(sample) - threshold) / ratio);
        }
        
        output[i] = sample;
    }
    return output;
};

// Convertir Float32 a Int16
const floatTo16BitPCM = (input) => {
    const output = new Int16Array(input.length);
    for (let i = 0; i < input.length; i++) {
        const s = Math.max(-1, Math.min(1, input[i]));
        output[i] = s < 0 ? s * 0x8000 : s * 0x7FFF;
    }
    return output.buffer;
};

const stopTransmitting = () => {
    if (processor) {
        processor.disconnect();
    }
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
    }
    if (audioContext) {
        audioContext.close();
    }
    if (ws) {
        ws.close();
    }
    transmitting.value = false;
    isConnecting.value = false;
    status.value = 'Detenido';
};
</script>

<style scoped>
.transmitter {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 15px;
    margin: 20px;
    padding: 20px;
    background: #f8f9fa;
    border-radius: 10px;
}

button {
    padding: 12px 24px;
    font-size: 16px;
    font-weight: bold;
    background-color: #3b82f6;
    color: white;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s;
    min-width: 160px;
}

button:hover:not(:disabled) {
    background-color: #2563eb;
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
    background-color: #dbeafe;
    color: #1e40af;
    font-weight: 500;
    min-width: 200px;
    text-align: center;
}

h2 {
    color: #1f2937;
    margin-bottom: 10px;
}
</style>